from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    environment: Literal["development", "production", "testing"] = "development"
    log_level: str = "INFO"
    api_version: str = "v1"
    host: str = "0.0.0.0"
    port: int = 8000
    max_cargo_count: int = 10000
    max_tank_count: int = 10000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
