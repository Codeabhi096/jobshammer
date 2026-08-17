import json
from pathlib import Path
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

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
    Filters out short matches that are just fragments of a longer match
    (e.g. standalone "C" getting matched inside "C++").
    """
    doc = nlp(text)
    matches = matcher(doc)

    # Sort by span length (longest first) so we can drop shorter matches
    # that sit right next to/inside a longer, more specific match
    spans = sorted(
        [(start, end, doc[start:end].text) for _, start, end in matches],
        key=lambda x: (x[1] - x[0]),
        reverse=True
    )

    kept = []
    occupied = set()
    for start, end, text_span in spans:
        token_range = set(range(start, end))
        # Skip if this span overlaps or sits directly adjacent to an already-kept longer span
        if token_range & occupied:
            continue
        touches_occupied = any((start - 1) in occupied or end in occupied for _ in [0])
        if touches_occupied:
            continue
        kept.append(text_span)
        occupied.update(token_range)

    return sorted(set(kept))