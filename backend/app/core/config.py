from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "AegisAI Enterprise Platform"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    # Databases and Cache
    DATABASE_URL: str = "postgresql+asyncpg://postgres:secure_password_123@localhost:5432/aegisai_db"
    REDIS_URL: str = "redis://:redis_password_123@localhost:6379/0"

    # JWT Security Secrets (Defaults for local development)
    JWT_SECRET_KEY: str = "super_secure_jwt_access_secret_key_change_me_in_production_9f2a71"
    JWT_REFRESH_SECRET_KEY: str = "super_secure_jwt_refresh_secret_key_change_me_in_production_8c3b12"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

settings = Settings()
