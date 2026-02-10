"""
Configuration module for SportMonks News API application.
Loads environment variables and provides app-wide settings.
"""

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    sportmonks_api_token: str = os.getenv("SPORTMONKS_API_TOKEN", "YOUR_TOKEN_HERE").strip('"').strip("'")
    fastapi_host: str = os.getenv("FASTAPI_HOST", "127.0.0.1")
    fastapi_port: int = int(os.getenv("FASTAPI_PORT", "8000"))

    # SportMonks base URL
    sportmonks_base_url: str = "https://api.sportmonks.com/v3/football"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
