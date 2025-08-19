from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8080

    # CORS
    api_cors_allow_all: bool = True
    # CSV w ENV: http://localhost:3000,http://frontend:3000
    api_cors_allow_origins: List[str] = []

    class Config:
        env_prefix = "API_"      # np. API_PORT, API_CORS_ALLOW_ALL
        case_sensitive = False

settings = Settings()
