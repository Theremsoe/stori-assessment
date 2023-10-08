from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseConfig(BaseSettings):
    """
    Database configuration
    """
    url: Optional[str] = None

    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 5432
    database: Optional[str] = 'forge'
    username: Optional[str] = 'forge'
    password: Optional[str] = ''

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_")
