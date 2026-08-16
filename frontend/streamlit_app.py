import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="JobsHammer", layout="centered")
st.title("JobsHammer — AI Career Coach")
st.write("Apna resume upload karo aur job description paste karo, match score aur skill gaps dekho.")

# ---- Resume Upload ----
st.header("1. Resume Upload")
resume_file = st.file_uploader("Resume (PDF)", type=["pdf"])

if "resume_id" not in st.session_state:
    st.session_state.resume_id = None

if resume_file and st.button("Upload Resume"):
    files = {"file": (resume_file.name, resume_file.getvalue(), "application/pdf")}
    response = requests.post(f"{API_URL}/upload-resume", files=files)

    if response.status_code == 200:
        data = response.json()
        st.session_state.resume_id = data["id"]
        st.success(f"Resume uploaded! (id: {data['id']})")
        st.write("**Extracted Skills:**", ", ".join(data["extracted_skills"]))
    else:
        st.error(f"Error: {response.text}")

# ---- Job Description ----
st.header("2. Job Description")
jd_text = st.text_area("Job Description paste karo", height=200)

if "jd_id" not in st.session_state:
    st.session_state.jd_id = None

if jd_text and st.button("Analyze Job"):
    response = requests.post(f"{API_URL}/analyze-job", json={"raw_text": jd_text})

    if response.status_code == 200:
        data = response.json()
        st.session_state.jd_id = data["id"]
        st.success(f"Job analyzed! (id: {data['id']})")
        st.write("**Extracted Requirements:**", ", ".join(data["extracted_requirements"]))
    else:
        st.error(f"Error: {response.text}")

# ---- Match ----
st.header("3. Match Score")

if st.button("Calculate Match"):
    if not st.session_state.resume_id or not st.session_state.jd_id:
        st.warning("Pehle resume upload karo aur job description analyze karo.")
    else:
        payload = {"resume_id": st.session_state.resume_id, "jd_id": st.session_state.jd_id}
        response = requests.post(f"{API_URL}/match", json=payload)

        if response.status_code == 200:
            data = response.json()
            st.metric("Match Score", f"{data['match_score']}%")

            if not data["skill_data_available"]:
                st.warning(
                    "Is job description me koi specific technical skill detect nahi hui — "
                    "score sirf overall semantic similarity par based hai, isliye kam reliable ho sakta hai."
                )

            st.caption(
                f"Embedding similarity: {data['embedding_score']}% | "
                f"Skill overlap: {data['skill_overlap_score']}%"
            )

            if data["missing_skills"]:
                st.write("**Missing Skills:**", ", ".join(data["missing_skills"]))
            else:
                st.write("**Missing Skills:** None found 🎉")
        else:
            st.error(f"Error: {response.text}")