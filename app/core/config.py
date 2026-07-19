from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    google_api_key: str = ""
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.7
    chunk_size: int = 1000
    chunk_overlap: int = 200
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    pdf_path: str = "Lectura.pdf"
    chroma_db_path: str = "chroma_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
