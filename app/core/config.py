from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        protected_namespaces=("settings_",),
    )

    cohere_api_key: str = ""
    model_name: str = "command-a-03-2025"
    temperature: float = 0.7
    chunk_size: int = 1000
    chunk_overlap: int = 200
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    pdf_path: str = "Lectura.pdf"


settings = Settings()
