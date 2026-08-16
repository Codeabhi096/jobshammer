import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")


SKILLS_LIST = [
    "Python", "SQL", "Machine Learning", "Deep Learning", "Scikit-learn",
    "PyTorch", "TensorFlow", "Computer Vision", "OpenCV", "YOLOv8",
    "NLP", "LLMs", "Generative AI", "RAG", "LangChain", "Hugging Face",
    "Prompt Engineering", "FAISS", "CrewAI", "Pandas", "NumPy",
    "Matplotlib", "Seaborn", "Power BI", "Tableau", "FastAPI",
    "Streamlit", "Django", "Flask", "Docker", "Git", "AWS", "MySQL"
]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in SKILLS_LIST]
matcher.add("SKILLS", patterns)


def extract_skills(text: str) -> list[str]:
    """
    Given raw resume/JD text, returns a de-duplicated list of matched skills.
    """
    doc = nlp(text)
    matches = matcher(doc)

    found_skills = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        found_skills.add(span.text)

    return sorted(found_skills)