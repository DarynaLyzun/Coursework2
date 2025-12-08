"""Loads configuration from environment variables.

This module uses Pydantic to validate and load settings defined in the 
.env file, making them accessible throughout the application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import MariaDBDsn, Field

class Settings(BaseSettings):
    """Application configuration settings.

    Attributes:
        database_url (MariaDBDsn): The connection string for the MariaDB database.
        openweather_api_key (str): A key for authorizing requests to the OpenWeatherMap API.
        secret_key (str): A secret string used to sign and verify JWT tokens.
        algorithm (str): The encryption algorithm used for JWTs (default: HS256).
        access_token_expire_minutes (int): The lifespan of an access token in minutes.
    """
    database_url: MariaDBDsn
    openweather_api_key: str = Field(pattern=r"^[a-fA-F0-9]{32}$")
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() # type: ignore