"""Configuration settings for the application.

This module handles loading and validating environment variables using Pydantic.
"""

from pydantic import Field, MariaDBDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings derived from environment variables.

    Attributes:
        database_url (MariaDBDsn): The database connection URL.
        openweather_api_key (str): API key for OpenWeatherMap (32 hex characters).
        secret_key (str): Secret key for JWT encoding and decoding.
        algorithm (str): The algorithm used for JWT encryption. Defaults to "HS256".
        access_token_expire_minutes (int): usage duration of access tokens. Defaults to 30.
    """

    database_url: MariaDBDsn
    openweather_api_key: str = Field(pattern=r"^[a-fA-F0-9]{32}$")
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() # type: ignore