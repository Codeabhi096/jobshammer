from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import db_models
from app.api.routes import resume, job, match, agent

app = FastAPI(title="JobsHammer")

Base.metadata.create_all(bind=engine)

app.include_router(resume.router, tags=["Resume"])
app.include_router(job.router, tags=["Job Description"])
app.include_router(match.router, tags=["Match"])
app.include_router(agent.router, tags=["Agent"])

@app.get("/")
def root():
    return {"status": "JobsHammer backend is alive"}