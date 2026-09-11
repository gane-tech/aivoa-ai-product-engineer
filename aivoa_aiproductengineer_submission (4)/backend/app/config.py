from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./aivoa_demo.db"
    ai_provider: str = "mock"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    max_text_chars: int = 12000
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

settings = Settings()
