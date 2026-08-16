from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.db_models import Resume, JobDescription, Match
from app.services.scoring import calculate_match_score, get_skill_gap
from app.schemas.schemas import MatchRequest, MatchResponse

router = APIRouter()


@router.post("/match", response_model=MatchResponse)
def create_match(payload: MatchRequest, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == payload.resume_id).first()
    jd = db.query(JobDescription).filter(JobDescription.id == payload.jd_id).first()

    if not resume or not jd:
        raise HTTPException(status_code=404, detail="Resume or Job Description not found")

    score = calculate_match_score(resume.raw_text, jd.raw_text)
    missing = get_skill_gap(resume.extracted_skills or [], jd.extracted_requirements or [])

    match = Match(
        resume_id=resume.id,
        jd_id=jd.id,
        match_score=score,
        gap_analysis=", ".join(missing)
    )
    db.add(match)
    db.commit()
    db.refresh(match)

    return MatchResponse(id=match.id, match_score=match.match_score, missing_skills=missing)