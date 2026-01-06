from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "Release Notes Manager"
    app_version: str = "1.0.0"
    debug: bool = True
    secret_key: str = "change-this-secret-key"

    host: str = "0.0.0.0"
    port: int = 8000

    database_url: str = "sqlite+aiosqlite:///./data/release_notes.db"

    ai_provider: str = "groq"

    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    groq_base_url: str = "https://api.groq.com/openai/v1"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    openai_base_url: str = "https://api.openai.com/v1"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-pro"

    jira_url: str = ""
    jira_email: str = ""
    jira_api_token: str = ""

    github_token: str = ""
    github_api_url: str = "https://api.github.com"
    github_org: str = "dnext-technology"

    confluence_url: str = ""
    confluence_email: str = ""
    confluence_api_token: str = ""
    confluence_space: str = "RELEASE"

    max_concurrent_jobs: int = 3
    job_timeout: int = 300
    job_cleanup_days: int = 30

    cors_origins: str = "http://localhost:8000,http://localhost:3000"

    max_upload_size: int = 10485760

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
