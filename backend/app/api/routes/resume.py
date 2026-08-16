import shutil
import tempfile
import os
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.db_models import Resume
from app.services.parser import extract_text_from_pdf
from app.services.nlp_extractor import extract_skills
from app.schemas.schemas import ResumeResponse

router = APIRouter()


@router.post("/upload-resume", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Uploaded file ko temporarily disk pe save karo taaki pdfplumber use kar sake
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    raw_text = extract_text_from_pdf(tmp_path)
    os.remove(tmp_path)  # temp file cleanup

    skills = extract_skills(raw_text)

    resume = Resume(raw_text=raw_text, extracted_skills=skills)
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume