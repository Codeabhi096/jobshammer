from numpy import dot
from numpy.linalg import norm
from app.services.embedding_service import get_embedding


def calculate_match_score(resume_text: str, jd_text: str) -> float:
    """
    Returns a similarity score between 0 and 100 based on cosine similarity
    of resume and job description embeddings.
    """
    resume_vec = get_embedding(resume_text)
    jd_vec = get_embedding(jd_text)

    cosine_sim = float(dot(resume_vec, jd_vec) / (norm(resume_vec) * norm(jd_vec)))
   

    # Cosine similarity is between -1 and 1; scale to 0-100 for readability
    score = round(((cosine_sim + 1) / 2) * 100, 2)
    return score


def get_skill_gap(resume_skills: list[str], jd_skills: list[str]) -> list[str]:
    """
    Returns skills present in the job description but missing from the resume.
    """
    resume_set = set(s.lower() for s in resume_skills)
    jd_set = set(s.lower() for s in jd_skills)

    missing = jd_set - resume_set
    return sorted(missing)