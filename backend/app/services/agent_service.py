from app.services.model_client import generate_response

INSTRUCTION = (
    "Analyze the candidate's resume against the job description. "
    "Identify the candidate's key strengths, weak areas, and specific "
    "improvements needed to be a stronger fit for this role."
)


def generate_gap_analysis(resume_text: str, jd_text: str) -> str:
    input_text = f"Resume:\n{resume_text[:3000]}\n\nJob Description:\n{jd_text[:2000]}"
    return generate_response(INSTRUCTION, input_text)