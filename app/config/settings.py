from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic Settings"""
    
    # API Settings
    PROJECT_NAME: str = "UANL Automation API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "uanl_db"
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Watson Orchestrate
    WATSON_API_KEY: Optional[str] = None
    WATSON_URL: Optional[str] = None
    WATSON_VERSION: str = "2023-09-01"
    
    # Email Settings
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # File uploads
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["pdf", "docx", "xlsx", "csv"]
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    @property
    def database_url_sync(self) -> str:
        """URL de base de datos síncrona"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql://")
    
    @property
    def database_url_async(self) -> str:
        """URL de base de datos asíncrona"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


# Instancia global de configuración
settings = Settings()
