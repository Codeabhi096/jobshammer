import sys
import json
import random
from pathlib import Path
import pandas as pd

BACKEND_PATH = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.insert(0, str(BACKEND_PATH))
from app.services.nlp_extractor import extract_skills  # noqa: E402

RAW_CSV = Path(__file__).resolve().parent / "raw" / "train.csv"
OUTPUT_JSONL = Path(__file__).resolve().parent / "processed" / "draft_dataset.jsonl"

TARGET_COUNT = 160          # final number of examples we want
MIN_RESUME_SKILLS = 3       # tech-relevance filter: resume must show at least this many skills
MIN_JD_SKILLS = 2           # JD must require at least this many skills
RANDOM_SEED = 42

INSTRUCTION = (
    "Analyze the candidate's resume against the job description. "
    "Identify the candidate's key strengths, weak areas, and specific "
    "improvements needed to be a stronger fit for this role."
)


def generate_draft_output(resume_skills, jd_skills):
    resume_set = set(s.lower() for s in resume_skills)
    jd_set = set(s.lower() for s in jd_skills)

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)

    strengths = ", ".join(matched[:5]) if matched else "no directly overlapping technical skills were clearly identified"
    output = f"Strengths: The candidate's background shows alignment with {strengths}.\n"

    if missing:
        weak_areas = ", ".join(missing[:5])
        output += f"Weak Areas: The role requires {weak_areas}, which are not clearly evidenced in the resume.\n"
        output += f"Improvement Suggestions: The candidate should highlight or build practical experience with {', '.join(missing[:3])} to strengthen their fit for this role."
    else:
        output += "Weak Areas: No major skill gaps were identified relative to the job description.\n"
        output += "Improvement Suggestions: The candidate appears well-aligned with this role's technical requirements."

    return output


def main():
    random.seed(RANDOM_SEED)
    df = pd.read_csv(RAW_CSV)
    df = df.dropna(subset=["resume_text", "job_description_text", "label"])

    # Deduplicate: keep only the FIRST occurrence of each unique resume and each unique JD
    # This maximizes diversity instead of seeing the same resume repeated across many rows
    df = df.drop_duplicates(subset=["resume_text"])
    df = df.drop_duplicates(subset=["job_description_text"])

    df = df.sample(frac=1, random_state=RANDOM_SEED)  # shuffle

    OUTPUT_JSONL.parent.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped_not_tech = 0

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            if written >= TARGET_COUNT:
                break

            resume_text = str(row["resume_text"])[:1500]
            jd_text = str(row["job_description_text"])[:1000]
            label = row["label"]

            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(jd_text)

            # Tech-relevance filter: skip roles with too few identifiable technical skills
            if len(resume_skills) < MIN_RESUME_SKILLS or len(jd_skills) < MIN_JD_SKILLS:
                skipped_not_tech += 1
                continue

            draft_output = generate_draft_output(resume_skills, jd_skills)

            example = {
                "instruction": INSTRUCTION,
                "input": f"Resume:\n{resume_text}\n\nJob Description:\n{jd_text}",
                "output": draft_output,
                "_meta_label": label,
            }

            f.write(json.dumps(example, ensure_ascii=False) + "\n")
            written += 1

    print(f"Done. {written} filtered, tech-relevant examples written to {OUTPUT_JSONL}")
    print(f"Skipped {skipped_not_tech} non-tech / low-signal rows during filtering.")


if __name__ == "__main__":
    main()