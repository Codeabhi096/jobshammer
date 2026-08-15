# JobsHammer

AI-powered Career Coach Agent — resume aur job description ka match score deta hai, skill gaps highlight karta hai, aur ek self-hosted fine-tuned LLM (no external API) se cover letter + improvement suggestions generate karta hai.

## Project Status
🚧 In active development — build log docs/ folder me milega.

## Stack
- Backend: FastAPI + SQLite/Postgres
- NLP: spaCy (skill extraction)
- Embeddings: sentence-transformers
- GenAI: Fine-tuned Qwen2.5-1.5B-Instruct (LoRA via Unsloth, trained on Google Colab)
- Frontend: Streamlit
- Hosting: Hugging Face Spaces (model + backend), free tier

## Folder Structure
See `docs/architecture.md` (coming soon)
