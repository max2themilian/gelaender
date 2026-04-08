from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Gelaender API"
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    database_url: str  # no default — fail loudly if absent
    allowed_origins: list[str] = ["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:3000"]
    google_calendar_ics_url: str | None = None
    google_calendar_id: str | None = None
    google_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
