import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Climate Health Advisory System API"
    API_V1_STR: str = "/api"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    OPENWEATHER_API_KEY: str

    DATABASE_URL: str
    SQLITE_FALLBACK_URL: str = "sqlite:///./climate_health.db"

    class Config:
        case_sensitive = True

settings = Settings()