from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.db_models import JobDescription
from app.services.nlp_extractor import extract_skills
from app.schemas.schemas import JobDescriptionCreate, JobDescriptionResponse

router = APIRouter()


@router.post("/analyze-job", response_model=JobDescriptionResponse)
def analyze_job(payload: JobDescriptionCreate, db: Session = Depends(get_db)):
    skills = extract_skills(payload.raw_text)

    jd = JobDescription(raw_text=payload.raw_text, extracted_requirements=skills)
    db.add(jd)
    db.commit()
    db.refresh(jd)

    return jd