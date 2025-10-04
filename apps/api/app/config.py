from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    cors_origins: str = "http://localhost:3000"
    api_secret_key: str = "devsecret"

    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "minio"
    minio_secret_key: str = "minio123"
    minio_bucket: str = "attachments"

    class Config:
        env_file = ".env"
        env_prefix = ""

settings = Settings()
