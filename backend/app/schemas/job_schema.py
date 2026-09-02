from pydantic import BaseModel, Field, field_validator


class JobCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    required_skills: list[str] = Field(min_length=1)
    preferred_skills: list[str] = Field(default_factory=list)
    minimum_experience_years: float | None = Field(default=None, ge=0)
    education_requirements: list[str] = Field(default_factory=list)
    required_certifications: list[str] = Field(default_factory=list)

    @field_validator(
        "required_skills",
        "preferred_skills",
        "education_requirements",
        "required_certifications",
    )
    @classmethod
    def validate_non_blank_items(cls, values: list[str]) -> list[str]:
        if any(not value.strip() for value in values):
            raise ValueError("List items cannot be blank")
        return values
