import unittest

from app.services.candidate_evaluation_service import evaluate_candidate
from app.services.skill_normalization import normalize_skill, normalized_skills


class CandidateEvaluationServiceTests(unittest.TestCase):
    def test_candidate_without_experience_warns_without_assuming_years(self):
        result = evaluate_candidate({"name": "Ana", "skills": ["Python"]})
        self.assertTrue(any("duration" in warning for warning in result["warnings"]))
        self.assertIn("experience", result["components"])

    def test_candidate_with_experience_scores_higher_than_empty_profile(self):
        experienced = evaluate_candidate({
            "name": "Ana", "skills": ["Python"], "experience_years": 4,
            "experience": [{"role": "Backend developer", "years": 4, "technologies": ["Python"]}],
        })
        empty = evaluate_candidate({"name": "Ana", "skills": ["Python"]})
        self.assertGreater(experienced["components"]["experience"], empty["components"]["experience"])

    def test_many_skills_without_evidence_are_not_automatically_strong(self):
        result = evaluate_candidate({"skills": [f"Skill {number}" for number in range(30)]})
        self.assertLess(result["components"]["technical_skills"], 40)
        self.assertTrue(result["warnings"])

    def test_detailed_projects_score_strongly(self):
        result = evaluate_candidate({
            "skills": ["Python", "Docker", "PostgreSQL"],
            "projects": [{"description": "Backend API with PostgreSQL, Docker, authentication, deployment and cloud architecture."}],
        })
        self.assertGreaterEqual(result["components"]["projects"], 75)

    def test_certifications_are_scored_from_present_evidence(self):
        result = evaluate_candidate({"certifications": ["AWS Certified Developer", "Microsoft Azure Fundamentals"]})
        self.assertGreater(result["components"]["certifications"], 60)

    def test_incomplete_candidate_has_low_cv_quality(self):
        result = evaluate_candidate({"name": "Ana"})
        self.assertLess(result["components"]["cv_quality"], 20)

    def test_unknown_information_keeps_score_bounded(self):
        result = evaluate_candidate({"name": "Ana", "summary": "Junior developer"})
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_classification_thresholds(self):
        strong = evaluate_candidate({
            "name": "Edgar Catalan", "email": "edgar@example.com", "phone": "1", "location": "GT",
            "summary": "Reduced processing time by 40%", "experience_years": 7,
            "skills": ["Python", "FastAPI", "MongoDB", "Docker"],
            "experience": [{"years": 7, "description": "Led Python API production systems"}],
            "projects": [{"description": "Python backend API, MongoDB, Docker, authentication and deployment"}],
            "education": ["Software Engineering Bachelor"],
            "certifications": ["AWS Certified Developer"],
        })
        self.assertIn(strong["classification"], {"Strong Candidate", "Excellent Candidate"})

    def test_grouped_skills_and_aliases_normalize(self):
        skills = normalized_skills(["Programming languages: Java · JavaScript · C# · Python · SQL", "NodeJS", "Postgres"])
        self.assertTrue({"java", "javascript", "c#", "python", "sql", "node.js", "postgresql"}.issubset(skills))
        self.assertEqual(normalize_skill(".NET 8"), ".net")

    def test_edgar_representative_cv_is_explainable(self):
        result = evaluate_candidate({
            "name": "Edgar Catalan", "experience_years": 2,
            "skills": ["Python", "FastAPI", "MongoDB", "Docker"],
            "experience": [{"years": 2, "description": "Built Python FastAPI APIs with MongoDB"}],
            "projects": [{"description": "Dockerized FastAPI backend with MongoDB"}],
        })
        self.assertTrue(result["strengths"])
        self.assertIsInstance(result["areas_to_improve"], list)


if __name__ == "__main__":
    unittest.main()
