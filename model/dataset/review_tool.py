import json
from pathlib import Path
import streamlit as st

DRAFT_FILE = Path(__file__).resolve().parent / "processed" / "draft_dataset.jsonl"
FINAL_FILE = Path(__file__).resolve().parent / "processed" / "train.jsonl"

st.set_page_config(page_title="Dataset Review Tool", layout="wide")
st.title("JobsHammer — Dataset Review Tool")

# ---- Load draft examples once ----
if "examples" not in st.session_state:
    with open(DRAFT_FILE, "r", encoding="utf-8") as f:
        st.session_state.examples = [json.loads(line) for line in f]
    st.session_state.index = 0
    st.session_state.kept = []

examples = st.session_state.examples
total = len(examples)

if st.session_state.index >= total:
    st.success(f"Review complete! {len(st.session_state.kept)} examples kept.")
    if st.button("Save Final Dataset"):
        with open(FINAL_FILE, "w", encoding="utf-8") as f:
            for ex in st.session_state.kept:
                ex.pop("_meta_label", None)  # remove review-only field before saving
                f.write(json.dumps(ex, ensure_ascii=False) + "\n")
        st.success(f"Saved {len(st.session_state.kept)} examples to {FINAL_FILE}")
    st.stop()

current = examples[st.session_state.index]

st.progress(st.session_state.index / total)
st.caption(f"Example {st.session_state.index + 1} of {total}  |  Kept so far: {len(st.session_state.kept)}  |  Label: {current.get('_meta_label', 'N/A')}")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Input (Resume + Job Description)")
    st.text_area("Input", current["input"], height=400, disabled=True, label_visibility="collapsed")

with col2:
    st.subheader("Output (edit this)")
    edited_output = st.text_area("Output", current["output"], height=400, label_visibility="collapsed")

col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button(" Keep", use_container_width=True):
        current["output"] = edited_output
        st.session_state.kept.append(current)
        st.session_state.index += 1
        st.rerun()

with col_b:
    if st.button("⏭️ Skip", use_container_width=True):
        st.session_state.index += 1
        st.rerun()

with col_c:
    if st.button("⬅️ Go Back", use_container_width=True):
        if st.session_state.index > 0:
            st.session_state.index -= 1
            if st.session_state.kept and st.session_state.kept[-1] is current:
                st.session_state.kept.pop()
        st.rerun()