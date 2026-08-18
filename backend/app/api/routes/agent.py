from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.db_models import Resume, JobDescription
from app.services.agent_service import generate_gap_analysis

router = APIRouter()


@router.post("/agent-analysis")
def agent_analysis(resume_id: int, jd_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()

    if not resume or not jd:
        raise HTTPException(status_code=404, detail="Resume or Job Description not found")

    analysis = generate_gap_analysis(resume.raw_text, jd.raw_text)
    return {"analysis": analysis}