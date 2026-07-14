from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Keys & Auth
    GOOGLE_GEMINI_API_KEY: Optional[str] = "mock_key"
    SECRET_KEY: str = "moodbowl_super_secret_jwt_key_999"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200 # 30 days for prototype persistence

    # Database & Redis
    DATABASE_URL: str = "sqlite+aiosqlite:///./moodbowl.db"
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Feature Flags & Modes
    MOCK_MODE: bool = True
    
    # Thresholds
    CONFIDENCE_THRESHOLD: float = 0.6
    INTENT_CONFIDENCE_THRESHOLD: float = 0.7
    GEMINI_TIMEOUT_SECONDS: float = 2.0
    
    # Rate Limiting
    RATE_LIMIT: str = "10/minute"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
