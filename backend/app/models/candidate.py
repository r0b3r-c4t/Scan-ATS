from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ResumeInfo(BaseModel):
    file_id: str
    filename: str
    content_type: str
    size: int


class ProcessingInfo(BaseModel):
    status: str = "uploaded"
    model: Optional[str] = None
    processed_at: Optional[datetime] = None


class Candidate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

    summary: Optional[str] = None

    skills: list[str] = Field(default_factory=list)

    experience: list[dict] = Field(default_factory=list)

    education: list[dict] = Field(default_factory=list)

    certifications: list[str] = Field(default_factory=list)

    resume: ResumeInfo

    processing: ProcessingInfo = Field(
        default_factory=ProcessingInfo
    )