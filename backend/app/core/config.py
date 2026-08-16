from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "JobsHammer"
    DATABASE_URL: str = "sqlite:///./jobshammer.db"

    class Config:
        env_file = ".env"

settings = Settings()