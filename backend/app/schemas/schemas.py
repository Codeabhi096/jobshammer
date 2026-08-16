from pydantic import BaseModel
from typing import List


class ResumeResponse(BaseModel):
    id: int
    extracted_skills: List[str]

    class Config:
        from_attributes = True


class JobDescriptionCreate(BaseModel):
    raw_text: str


class JobDescriptionResponse(BaseModel):
    id: int
    extracted_requirements: List[str]

    class Config:
        from_attributes = True


class MatchRequest(BaseModel):
    resume_id: int
    jd_id: int


class MatchResponse(BaseModel):
    id: int
    match_score: float
    missing_skills: List[str]