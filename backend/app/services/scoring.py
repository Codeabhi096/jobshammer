from numpy import dot
from numpy.linalg import norm
from app.services.embedding_service import get_embedding


def calculate_embedding_score(resume_text: str, jd_text: str) -> float:
    resume_vec = get_embedding(resume_text)
    jd_vec = get_embedding(jd_text)

    cosine_sim = float(dot(resume_vec, jd_vec) / (norm(resume_vec) * norm(jd_vec)))
    # Coherent professional text rarely gives negative cosine similarity,
    # so the old (cos+1)/2 scaling compressed everything into a narrow high band.
    # Using raw cosine * 100 gives a wider, more discriminative range.
    score = max(cosine_sim, 0) * 100
    return round(score, 2)


def get_skill_gap(resume_skills: list[str], jd_skills: list[str]) -> list[str]:
    resume_set = set(s.lower() for s in resume_skills)
    jd_set = set(s.lower() for s in jd_skills)
    missing = jd_set - resume_set
    return sorted(missing)


def calculate_final_score(resume_text: str, jd_text: str, resume_skills: list[str], jd_skills: list[str]) -> dict:
    """
    Combines semantic embedding similarity with explicit skill overlap
    for a more reliable, discriminative match score.
    """
    embedding_score = calculate_embedding_score(resume_text, jd_text)

    if jd_skills:
        overlap_count = len(set(s.lower() for s in resume_skills) & set(s.lower() for s in jd_skills))
        skill_overlap_score = round((overlap_count / len(jd_skills)) * 100, 2)
        final_score = round(0.5 * embedding_score + 0.5 * skill_overlap_score, 2)
        skill_data_available = True
    else:
        # JD had no identifiable technical skills — score relies on embedding alone,
        # flagged so the UI can show a caveat instead of pretending it's fully reliable
        final_score = embedding_score
        skill_overlap_score = None
        skill_data_available = False

    return {
        "final_score": final_score,
        "embedding_score": embedding_score,
        "skill_overlap_score": skill_overlap_score,
        "skill_data_available": skill_data_available,
    }