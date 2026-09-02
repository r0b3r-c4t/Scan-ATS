import re
from typing import Any

from app.services.skill_normalization import SKILL_ALIASES, normalize_skill


class MatchingService:
    """Deterministic, explainable candidate-to-job scoring."""

    WEIGHTS = {
        "required_skills": 0.50,
        "preferred_skills": 0.10,
        "experience": 0.15,
        "education": 0.10,
        "certifications": 0.05,
        "projects": 0.10,
    }

    SKILL_ALIASES = SKILL_ALIASES

    @classmethod
    def calculate_match(cls, candidate: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
        required_skills = cls._unique_strings(job.get("required_skills", []))
        preferred_skills = cls._unique_strings(job.get("preferred_skills", []))
        candidate_skills = cls._normalized_skill_set(candidate.get("skills", []))

        matched_required, missing_required = cls._split_skills(required_skills, candidate_skills)
        matched_preferred, missing_preferred = cls._split_skills(preferred_skills, candidate_skills)

        required_score = cls._ratio_score(len(matched_required), len(required_skills))
        preferred_score = cls._ratio_score(len(matched_preferred), len(preferred_skills))

        minimum_years = job.get("minimum_experience_years")
        candidate_years = cls._experience_years(candidate)
        experience_applicable = minimum_years is not None and float(minimum_years) > 0
        experience_score = (
            cls._ratio_score(candidate_years, float(minimum_years))
            if experience_applicable and candidate_years is not None
            else 100
        )

        education_requirements = cls._unique_strings(job.get("education_requirements", []))
        education_score = cls._text_requirement_score(
            candidate.get("education", []), education_requirements
        ) if education_requirements else 100

        certification_requirements = cls._unique_strings(job.get("required_certifications", []))
        certifications_score = cls._text_requirement_score(
            candidate.get("certifications", []), certification_requirements
        ) if certification_requirements else 100

        project_terms = cls._unique_strings(required_skills + preferred_skills)
        projects_score = cls._project_score(candidate.get("projects", []), project_terms)

        component_scores = {
            "required_skills": required_score,
            "preferred_skills": preferred_score,
            "experience": experience_score,
            "education": education_score,
            "certifications": certifications_score,
            "projects": projects_score,
        }
        applicable = {
            "required_skills": bool(required_skills),
            "preferred_skills": bool(preferred_skills),
            "experience": experience_applicable and candidate_years is not None,
            "education": bool(education_requirements),
            "certifications": bool(certification_requirements),
            "projects": bool(project_terms),
        }
        active_weight = sum(cls.WEIGHTS[name] for name, enabled in applicable.items() if enabled)
        weighted_score = sum(
            component_scores[name] * cls.WEIGHTS[name]
            for name, enabled in applicable.items()
            if enabled
        )
        match_percentage = round(weighted_score / active_weight) if active_weight else 0
        match_percentage = max(0, min(100, match_percentage))

        return {
            "match_percentage": match_percentage,
            "classification": cls._classification(match_percentage),
            "matched_skills": matched_required,
            "missing_required_skills": missing_required,
            "matched_preferred_skills": matched_preferred,
            "missing_preferred_skills": missing_preferred,
            "experience_score": round(experience_score),
            "skills_score": round(required_score),
            "preferred_skills_score": round(preferred_score),
            "education_score": round(education_score),
            "certifications_score": round(certifications_score),
            "projects_score": round(projects_score),
            "explanation": cls._explanation(
                matched_required, missing_required, matched_preferred,
                missing_preferred, candidate_years, minimum_years, applicable
            ),
        }

    @classmethod
    def normalize_skill(cls, value: str) -> str:
        return normalize_skill(value)

    @classmethod
    def _normalized_skill_set(cls, values: Any) -> set[str]:
        result = set()
        for value in values if isinstance(values, list) else []:
            if isinstance(value, str) and value.strip():
                result.add(cls.normalize_skill(value))
            elif isinstance(value, dict):
                for key in ("name", "skill", "technology"):
                    item = value.get(key)
                    if isinstance(item, str) and item.strip():
                        result.add(cls.normalize_skill(item))
        return result

    @classmethod
    def _split_skills(cls, requested: list[str], available: set[str]) -> tuple[list[str], list[str]]:
        matched, missing = [], []
        for skill in requested:
            (matched if cls.normalize_skill(skill) in available else missing).append(skill)
        return matched, missing

    @classmethod
    def _experience_years(cls, candidate: dict[str, Any]) -> float | None:
        direct_years = candidate.get("experience_years")
        if isinstance(direct_years, (int, float)) and direct_years >= 0:
            return float(direct_years)

        total = 0.0
        found = False
        for item in candidate.get("experience", []) if isinstance(candidate.get("experience"), list) else []:
            if not isinstance(item, dict):
                continue
            years = item.get("years", item.get("duration_years"))
            if isinstance(years, (int, float)) and years >= 0:
                total += float(years)
                found = True
        return total if found else None

    @classmethod
    def _text_requirement_score(cls, candidate_values: Any, requirements: list[str]) -> float:
        candidate_text = cls._flatten_text(candidate_values)
        matches = sum(
            1 for requirement in requirements
            if cls.normalize_skill(requirement) in cls.normalize_skill(candidate_text)
        )
        return cls._ratio_score(matches, len(requirements))

    @classmethod
    def _project_score(cls, projects: Any, job_terms: list[str]) -> float:
        if not job_terms:
            return 100
        project_text = cls._flatten_text(projects)
        normalized_project = cls.normalize_skill(project_text)
        matches = sum(1 for term in job_terms if cls.normalize_skill(term) in normalized_project)
        return cls._ratio_score(matches, len(job_terms))

    @staticmethod
    def _flatten_text(value: Any) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return " ".join(MatchingService._flatten_text(item) for item in value.values())
        if isinstance(value, list):
            return " ".join(MatchingService._flatten_text(item) for item in value)
        return ""

    @staticmethod
    def _ratio_score(matched: float, total: float) -> float:
        return min(100.0, (matched / total) * 100) if total else 100.0

    @staticmethod
    def _unique_strings(values: Any) -> list[str]:
        unique, seen = [], set()
        for value in values if isinstance(values, list) else []:
            if isinstance(value, str) and value.strip():
                key = MatchingService.normalize_skill(value)
                if key not in seen:
                    seen.add(key)
                    unique.append(value.strip())
        return unique

    @staticmethod
    def _classification(score: int) -> str:
        if score >= 90:
            return "Excellent Match"
        if score >= 75:
            return "Strong Match"
        if score >= 60:
            return "Moderate Match"
        if score >= 40:
            return "Weak Match"
        return "Poor Match"

    @staticmethod
    def _explanation(
        matched: list[str], missing: list[str], preferred_matched: list[str],
        preferred_missing: list[str], candidate_years: float | None,
        minimum_years: Any, applicable: dict[str, bool]
    ) -> str:
        parts = [f"Cumple {len(matched)} de {len(matched) + len(missing)} habilidades requeridas."]
        if missing:
            parts.append("Faltan: " + ", ".join(missing) + ".")
        if preferred_matched or preferred_missing:
            parts.append(
                f"Cumple {len(preferred_matched)} de "
                f"{len(preferred_matched) + len(preferred_missing)} habilidades preferidas."
            )
        if minimum_years is not None:
            if candidate_years is None:
                parts.append("No hay años de experiencia verificables; este componente no se aplicó.")
            else:
                parts.append(f"Experiencia verificable: {candidate_years:g} de {float(minimum_years):g} años requeridos.")
        ignored = [name.replace("_", " ") for name, enabled in applicable.items() if not enabled]
        if ignored:
            parts.append("Pesos redistribuidos para componentes no aplicables: " + ", ".join(ignored) + ".")
        return " ".join(parts)
