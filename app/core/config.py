"""
Application Configuration
Zero-trust security settings and environment variables
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings with zero-trust defaults"""
    
    # Application
    APP_NAME: str = "Geo-fencing Platform"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Security - Zero Trust
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    TOKEN_ROTATION_ENABLED: bool = True
    
    # CORS - Strict by default (comma-separated string for env var compatibility)
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:3003"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "GET,POST,PUT,PATCH,DELETE"
    CORS_ALLOW_HEADERS: str = "*"
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS_ORIGINS string into list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    def get_cors_methods(self) -> List[str]:
        """Parse CORS_ALLOW_METHODS string into list"""
        return [method.strip() for method in self.CORS_ALLOW_METHODS.split(",")]
    
    def get_cors_headers(self) -> List[str]:
        """Parse CORS_ALLOW_HEADERS string into list"""
        if self.CORS_ALLOW_HEADERS == "*":
            return ["*"]
        return [header.strip() for header in self.CORS_ALLOW_HEADERS.split(",")]
    
    # Database - Default to SQLite for quick start
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./geofence_dev.db")
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_PRE_PING: bool = True
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_TTL_DEFAULT: int = 3600
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # AI/LLM Service
    OPENAI_API_KEY: Optional[str] = None
    AI_SERVICE_ENABLED: bool = True
    AI_MODEL: str = "gpt-4-turbo-preview"
    AI_TEMPERATURE: float = 0.7
    
    # Geospatial
    DEFAULT_SRID: int = 4326  # WGS84
    MAX_GEOFENCE_POINTS: int = 1000
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
