from pydantic import BaseModel


class MatchResultSchema(BaseModel):
    candidate_id: str
    job_id: str
    match_percentage: int
    classification: str
    matched_skills: list[str]
    missing_required_skills: list[str]
    matched_preferred_skills: list[str]
    missing_preferred_skills: list[str]
    experience_score: int
    skills_score: int
    preferred_skills_score: int
    education_score: int
    certifications_score: int
    projects_score: int
    explanation: str
