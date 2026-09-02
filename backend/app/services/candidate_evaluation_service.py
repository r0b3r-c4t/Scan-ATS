import re
from typing import Any
from datetime import datetime

from app.services.skill_normalization import normalize_skill, normalized_skills, skill_has_evidence


class CandidateEvaluationService:
    WEIGHTS = {
        "experience": 0.25, "technical_skills": 0.20, "projects": 0.15,
        "education": 0.10, "certifications": 0.10, "achievements": 0.10,
        "cv_quality": 0.05, "consistency": 0.05,
    }

    @classmethod
    def evaluate_candidate(cls, candidate: dict[str, Any]) -> dict[str, Any]:
        print("\n=== CANDIDATE EVALUATION START ===")
        print(f"Candidate name: {candidate.get('name', 'N/A')}")
        
        warnings: list[str] = []
        
        # Calculate all component scores
        experience, experience_known = cls._experience_score(candidate, warnings)
        print(f"Experience score: {experience} (known: {experience_known})")
        
        skills, skill_evidence = cls._skill_score(candidate)
        print(f"Technical skills score: {skills} (evidence ratio: {skill_evidence})")
        
        projects = cls._project_score(candidate.get("projects", []))
        print(f"Projects score: {projects}")
        
        education = cls._education_score(candidate.get("education", []))
        print(f"Education score: {education}")
        
        certifications = cls._certification_score(candidate.get("certifications", []))
        print(f"Certifications score: {certifications}")
        
        achievements = cls._achievement_score(candidate)
        print(f"Achievements score: {achievements}")
        
        cv_quality = cls._cv_quality_score(candidate)
        print(f"CV Quality score: {cv_quality}")
        
        consistency = cls._consistency_score(candidate, skill_evidence)
        print(f"Consistency score: {consistency}")
        
        components = {
            "experience": experience,
            "technical_skills": skills,
            "projects": projects,
            "education": education,
            "certifications": certifications,
            "achievements": achievements,
            "cv_quality": cv_quality,
            "consistency": consistency,
        }
        
        # Determine which components are applicable
        applicable = {name: True for name in components}
        if not experience_known:
            applicable["experience"] = False
            print("Note: Experience is not applicable (duration could not be determined)")
        
        # Calculate weighted score using only applicable components
        active_weight = sum(cls.WEIGHTS[key] for key, enabled in applicable.items() if enabled)
        if active_weight == 0:
            score = 50
        else:
            score = round(sum(components[key] * cls.WEIGHTS[key] for key in components if applicable[key]) / active_weight)
        
        score = max(0, min(100, score))
        print(f"Final score: {score}")
        print("=== CANDIDATE EVALUATION END ===\n")
        
        strengths = cls._strengths(components, candidate, skill_evidence)
        improvements = cls._improvements(components, experience_known)
        
        if skill_evidence == 0 and normalized_skills(candidate.get("skills", [])):
            warnings.append("Declared skills have no supporting evidence in experience, projects, education, or certifications.")
        
        return {
            "score": score,
            "classification": cls._classification(score),
            "components": {key: round(value) for key, value in components.items()},
            "strengths": strengths,
            "areas_to_improve": improvements,
            "warnings": warnings,
        }

    @staticmethod
    def _flatten(value: Any) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return " ".join(CandidateEvaluationService._flatten(item) for item in value.values())
        if isinstance(value, list):
            return " ".join(CandidateEvaluationService._flatten(item) for item in value)
        return ""

    @classmethod
    def _parse_date_string(cls, date_str: str) -> float | None:
        """
        Parse date strings like:
        - "NOVIEMBRE 2022 - A LA FECHA" (current)
        - "ENERO 2020 - NOVIEMBRE 2022"
        - "2020 - 2022"
        Returns approximate years of experience, or None if cannot parse.
        """
        if not isinstance(date_str, str):
            return None
        
        date_str = date_str.strip()
        
        # Try to extract years using regex
        # Look for patterns like "2022", "2020"
        year_matches = re.findall(r'\b(20\d{2}|19\d{2})\b', date_str)
        
        if not year_matches:
            return None
        
        # Check if currently working (contains "present", "current", "la fecha", "today", "now", etc.)
        is_current = any(term in date_str.lower() for term in [
            'a la fecha', 'present', 'current', 'today', 'now', 'presente', 
            'actualidad', 'actualmente', 'ongoing'
        ])
        
        if len(year_matches) >= 2:
            try:
                start_year = int(year_matches[0])
                end_year = int(year_matches[1])
                duration = end_year - start_year
                return float(max(0.5, duration))  # Minimum 6 months
            except (ValueError, IndexError):
                pass
        elif len(year_matches) == 1:
            # Only one year found - assume it's start year
            try:
                start_year = int(year_matches[0])
                current_year = datetime.now().year
                if is_current:
                    duration = current_year - start_year + 1
                    return float(max(0.5, duration))
                else:
                    # Just one year, no end date, not current = very recent
                    return 0.5
            except ValueError:
                pass
        
        return None

    @classmethod
    def _experience_score(cls, candidate: dict, warnings: list[str]) -> tuple[float, bool]:
        items = candidate.get("experience", [])
        
        # Try to get direct years if available
        direct = candidate.get("experience_years")
        years = float(direct) if isinstance(direct, (int, float)) and direct >= 0 else None
        
        # If not directly provided, calculate from experience items
        if years is None and isinstance(items, list):
            total_years = 0.0
            years_found = False
            
            for item in items:
                if isinstance(item, dict):
                    # Try to get years from multiple possible field names
                    item_years = item.get("years") or item.get("duration_years") or item.get("duration")
                    
                    if isinstance(item_years, (int, float)) and item_years >= 0:
                        total_years += float(item_years)
                        years_found = True
                    else:
                        # Try to parse from dates field
                        dates_str = item.get("dates") or item.get("date") or item.get("period")
                        if dates_str:
                            parsed_years = cls._parse_date_string(dates_str)
                            if parsed_years is not None:
                                total_years += parsed_years
                                years_found = True
            
            if years_found:
                years = total_years
        
        # If still no years found, check if we have experience items at least
        if years is None:
            if items and len(items) > 0:
                # Has experience but duration unknown - default to 65
                warnings.append("Professional experience duration could not be determined from the CV.")
                return (65.0, False)
            else:
                # No experience at all
                return (0.0, False)
        
        # Calculate score based on years
        # Base: 35 + (years * 13)
        base = min(100.0, 35 + years * 13)
        
        # Bonus for seniority indicators and complex responsibilities
        detail = cls._flatten(items).lower()
        seniority_terms = (
            "led", "lider", "jefe", "gerente", "subgerente", "director", 
            "coordinador", "supervisor", "manager", "arquitectura", "arquitecto",
            "lead", "senior"
        )
        seniority_bonus = min(10, 2.5 * sum(term in detail for term in seniority_terms))
        
        complexity_bonus = 0
        if any(term in detail for term in ("producción", "production", "deploy", "api", "database", "base de datos")):
            complexity_bonus = 3
        
        final_score = min(100.0, base + seniority_bonus + complexity_bonus)
        return (final_score, True)

    @classmethod
    def _skill_score(cls, candidate: dict) -> tuple[float, float]:
        """
        Score skills based on:
        1. Number of skills declared
        2. Evidence of skills in experience/projects/education
        """
        skills = normalized_skills(candidate.get("skills", []))
        
        if not skills:
            return 0.0, 0.0
        
        # Get evidence from all sections
        evidence_text = cls._flatten([
            candidate.get("experience", []),
            candidate.get("projects", []),
            candidate.get("education", []),
            candidate.get("certifications", []),
        ]).lower()
        
        # Check how many skills have evidence
        evidenced = {skill for skill in skills if skill_has_evidence(skill, evidence_text)}
        
        # Score based on skill count and evidence
        # More skills = higher coverage (but diminishing returns)
        coverage = min(35.0, len(skills) * 5.0)
        
        # Evidence portion based on how many declared skills are evidenced
        evidence_ratio = len(evidenced) / len(skills) if skills else 0
        evidence = 65.0 * evidence_ratio
        
        final_score = min(100.0, coverage + evidence)
        
        return final_score, evidence_ratio

    @classmethod
    def _project_score(cls, projects: Any) -> float:
        if not isinstance(projects, list) or not projects:
            return 0.0
        text = cls._flatten(projects).lower()
        complexity_terms = ("api", "backend", "frontend", "database", "docker", "authentication", "deploy", "cloud", "architecture", "microservice")
        complexity = min(55.0, sum(term in text for term in complexity_terms) * 7.0)
        detail = min(25.0, sum(bool(cls._flatten(project)) for project in projects) * 8.0)
        variety = min(20.0, len(normalized_skills([cls._flatten(projects)])) * 2.0)
        return min(100.0, 20.0 + complexity + detail + variety)

    @classmethod
    def _education_score(cls, education: Any) -> float:
        """
        Evaluate education based on degree type, field, and honors.
        Handles text like "Licenciatura en Administración | Magna Cum Laude"
        """
        text = cls._flatten(education).lower()
        
        if not text:
            return 0.0
        
        # Base score by education level
        degree_levels = [
            ("phd", 95),
            ("doctor", 95),
            ("doctorado", 95),
            ("master", 88),
            ("maestr", 88),
            ("especialización", 85),
            ("specialization", 85),
            ("bachelor", 82),
            ("licenc", 82),
            ("ingenie", 80),
            ("técnico universitario", 78),
            ("tecnic", 75),
            ("diploma", 70),
            ("course", 55),
            ("curso", 55),
            ("certification", 50),
            ("certificación", 50),
        ]
        
        base_score = 60  # Default base
        for degree_term, score in degree_levels:
            if degree_term in text:
                base_score = score
                break
        
        # Add points for honors/distinctions
        honors_bonus = 0
        honors_terms = {
            "magna cum laude": 15,
            "cum laude": 10,
            "suma cum laude": 12,
            "summa cum laude": 12,
            "honors": 8,
            "distinción": 8,
            "premio académico": 8,
        }
        for honor, bonus in honors_terms.items():
            if honor in text:
                honors_bonus = max(honors_bonus, bonus)
                break  # Only count the highest honor
        
        # Add points for technical/relevant fields
        field_bonus = 0
        relevant_fields = (
            "software", "computer", "comput", "informatic", "tecnolog", 
            "ingeniería", "engineering", "administración", "business",
            "finanzas", "finance", "contabilidad", "accounting", 
            "marketing", "gestión", "management"
        )
        if any(field in text for field in relevant_fields):
            field_bonus = 5
        
        final_score = min(100.0, base_score + honors_bonus + field_bonus)
        return final_score

    @classmethod
    def _certification_score(cls, certifications: Any) -> float:
        if not isinstance(certifications, list) or not certifications:
            return 0.0
        text = cls._flatten(certifications).lower()
        score = min(75.0, 35 + len(certifications) * 20)
        if any(term in text for term in ("aws", "microsoft", "google", "cisco", "oracle", "comptia", "scrum")):
            score += 15
        return min(100.0, score)

    @classmethod
    def _achievement_score(cls, candidate: dict) -> float:
        """
        Detect achievements from summary, experience, and projects.
        Look for quantified metrics, outcomes, and leadership evidence.
        """
        text = cls._flatten([
            candidate.get("summary", ""),
            candidate.get("experience", []),
            candidate.get("projects", [])
        ]).lower()
        
        # Detect quantified metrics
        # Look for patterns like: 95%, Q2 millones, 88% eficacia, etc.
        quantified_patterns = [
            r'\d+\s*%',  # Percentages: 95%, 88%
            r'[qQ]\s*\d+',  # Q notation: Q2
            r'\d+\s*(?:millones?|millón|usuarios?|customers?|clientes?|employees?)',  # Numbers with units
            r'[€₹$£]\s*\d+',  # Currency amounts
            r'\d+\.\d+\s*(?:millones?|mil)',  # Decimal millions: 2.5 millones
        ]
        has_quantified = any(re.search(pattern, text) for pattern in quantified_patterns)
        
        # Detect outcome-oriented language
        outcome_terms = (
            "reducción", "reduced", "increment", "incremento", "aumento", "increased",
            "mejora", "improved", "optimization", "optimización", "eficacia", "efficiency",
            "logré", "logrando", "achievement", "accomplished", "award", "premio",
            "recognition", "reconocimiento", "certification", "implementación", "implementation"
        )
        has_outcome = any(term in text for term in outcome_terms)
        
        # Detect leadership/impact
        leadership_terms = (
            "led", "lideré", "liderando", "lider", "mentor", "mentored", "mentoriz",
            "supervise", "supervised", "manage", "managed", "director", "gerente"
        )
        has_leadership = any(term in text for term in leadership_terms)
        
        # Detect production/operational impact
        has_production_impact = any(term in text for term in ("production", "producción", "operaciones", "operations"))
        
        # Score calculation
        score = 0.0
        
        # Base for quantified + outcome (strong evidence)
        if has_quantified and has_outcome:
            score += 50
        elif has_quantified or has_outcome:
            score += 35  # Either quantified or outcome is still meaningful
        
        # Bonus for leadership
        if has_leadership:
            score += 20
        
        # Bonus for production/operational impact
        if has_production_impact:
            score += 15
        
        # Bonus for multiple achievements
        achievement_count = len(re.findall(r'\d+\s*%', text))  # Count of percentage-based achievements
        score += min(15, achievement_count * 5)
        
        return min(100.0, score)

    @staticmethod
    def _cv_quality_score(candidate: dict) -> float:
        fields = ("name", "email", "phone", "location", "summary", "skills", "experience", "education", "projects", "certifications")
        return 100.0 * sum(bool(candidate.get(field)) for field in fields) / len(fields)

    @classmethod
    def _consistency_score(cls, candidate: dict, evidence_ratio: float) -> float:
        skills = normalized_skills(candidate.get("skills", []))
        if not skills:
            return 25.0
        return 25.0 + evidence_ratio * 75.0

    @staticmethod
    def _classification(score: int) -> str:
        if score >= 90: return "Excellent Candidate"
        if score >= 75: return "Strong Candidate"
        if score >= 60: return "Moderate Candidate"
        if score >= 40: return "Weak Candidate"
        return "Poor Candidate"

    @staticmethod
    def _strengths(components: dict, candidate: dict, evidence_ratio: float) -> list[str]:
        strengths = []
        if components["technical_skills"] >= 75: strengths.append("Strong technical skill coverage")
        if components["projects"] >= 75: strengths.append("Multiple or technically detailed software projects")
        if components["experience"] >= 75: strengths.append("Demonstrated professional experience")
        if components["achievements"] >= 70: strengths.append("Quantified impact or achievement evidence")
        if evidence_ratio >= 0.7: strengths.append("Skills are supported by experience or project evidence")
        return strengths

    @staticmethod
    def _improvements(components: dict, experience_known: bool) -> list[str]:
        items = []
        if not experience_known: items.append("Professional experience duration is not documented")
        elif components["experience"] < 60: items.append("Limited professional experience")
        if components["projects"] < 50: items.append("Limited project evidence")
        if components["certifications"] < 50: items.append("Limited certification coverage")
        if components["achievements"] < 50: items.append("Few quantified achievements")
        if components["cv_quality"] < 70: items.append("CV is missing key profile sections")
        return items


def evaluate_candidate(candidate: dict) -> dict:
    return CandidateEvaluationService.evaluate_candidate(candidate)
