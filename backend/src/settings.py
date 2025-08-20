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

    # MQTT
    mqtt_url: str = "mqtt://mosquitto:1883"  # np. mqtt://user:pass@mosquitto:1883
    mqtt_client_id: str | None = None  # jak None -> we will generate a random

    # Shadow / offline
    shadow_offline_after_sec: int = 60  # ~2× heartbeat 30 s
    shadow_sweep_interval_sec: int = 5

    class Config:
        env_prefix = "API_"      # np. API_PORT, API_CORS_ALLOW_ALL
        case_sensitive = False

settings = Settings()
