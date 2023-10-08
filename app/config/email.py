from pydantic_settings import BaseSettings, SettingsConfigDict

class EmailConfig(BaseSettings):
    """
    Email base configuration
    """
    host: str = 'smtp.gmail.com'
    port: int = 587
    tls: bool = True
    ssl: bool = False
    user: str
    password: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="MAIL_")
