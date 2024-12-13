from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    SUPABASE_PUBLIC_KEY: str
    SUPABASE_SECRET_KEY: str
    SUPABASE_URL: str
    APP_ENVIRONMENT: str = 'LOCAL'
    CHROMA_COLLECTION: str = 'LOCAL'

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
