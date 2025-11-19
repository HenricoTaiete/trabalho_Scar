# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    # Database
    DATABASE_HOST: str = "db"
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = "Henrico"
    DATABASE_PASSWORD: str = "7bWRSFLouFD7LeqERQmfKyybWtqfRMLFCRSrB3ZY13hAVBfvYTYarFzOiGUbr1q3"
    DATABASE_NAME: str = "rfid_db"

    # JWT and Security
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}?charset=utf8mb4"
        )

# Instância global
settings = Settings()