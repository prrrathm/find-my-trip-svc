# swappable base_urls / models / search backend

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    search_xng_url: str
    agent_url: str
    agent_api_key: str
    agent_model: str = "llama3.2"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
