from pydantic import BaseModel
from typing import Any, Optional


class CandidateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    skills: list[str] = []
    experience: list = []
    education: list = []
    certifications: list = []
    projects: list = []
    candidate_score: Optional[dict[str, Any]] = None
