from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import db_models

app = FastAPI(title="JobsHammer")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "JobsHammer backend is alive"}