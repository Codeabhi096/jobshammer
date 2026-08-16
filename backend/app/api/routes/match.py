from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.db_models import Resume, JobDescription, Match
from app.services.scoring import calculate_final_score, get_skill_gap
from app.schemas.schemas import MatchRequest, MatchResponse

router = APIRouter()


@router.post("/match", response_model=MatchResponse)
def create_match(payload: MatchRequest, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == payload.resume_id).first()
    jd = db.query(JobDescription).filter(JobDescription.id == payload.jd_id).first()

    if not resume or not jd:
        raise HTTPException(status_code=404, detail="Resume or Job Description not found")

    resume_skills = resume.extracted_skills or []
    jd_skills = jd.extracted_requirements or []

    result = calculate_final_score(resume.raw_text, jd.raw_text, resume_skills, jd_skills)
    missing = get_skill_gap(resume_skills, jd_skills)

    match = Match(
        resume_id=resume.id,
        jd_id=jd.id,
        match_score=result["final_score"],
        gap_analysis=", ".join(missing)
    )
    db.add(match)
    db.commit()
    db.refresh(match)

    return MatchResponse(
        id=match.id,
        match_score=result["final_score"],
        embedding_score=result["embedding_score"],
        skill_overlap_score=result["skill_overlap_score"],
        skill_data_available=result["skill_data_available"],
        missing_skills=missing
    )