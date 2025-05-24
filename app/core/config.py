"""Configuration settings for the application."""

import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    database_url: str = os.getenv("DATABASE_URL", "")
    mysql_user: str = os.getenv("MYSQL_USER", "root")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "")
    mysql_host: str = os.getenv("MYSQL_HOST", "localhost")
    mysql_port: str = os.getenv("MYSQL_PORT", "3306")
    mysql_database: str = os.getenv("MYSQL_DATABASE", "se_challenge")

    api_v1_str: str = "/api/v1"
    project_name: str = "User Management API"
    project_version: str = "1.0.0"

    backend_cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    log_level: str = "INFO"

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
