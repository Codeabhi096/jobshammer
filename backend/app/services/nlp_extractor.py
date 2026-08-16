import json
from pathlib import Path
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

# Load skills from external JSON (categorized), flatten into one list
SKILLS_FILE = Path(__file__).resolve().parent.parent / "data" / "skills.json"

with open(SKILLS_FILE, "r", encoding="utf-8") as f:
    skills_by_category = json.load(f)

SKILLS_LIST = [skill for category in skills_by_category.values() for skill in category]

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