"""Unit tests for configuration loading."""

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from app.core.config import Settings

VALID_ENV = {
    "DATABASE_URL": "mariadb+mariadbconnector://user:pass@localhost:3306/test_db",
    "OPENWEATHER_API_KEY": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
    "SECRET_KEY": "supersecretkey123",
}


def test_settings_load_correctly():
    """Verifies correct loading of valid environment variables."""
    with patch.dict(os.environ, VALID_ENV, clear=True):
        settings = Settings(_env_file=None) # type: ignore

        assert str(settings.database_url) == VALID_ENV["DATABASE_URL"]
        assert settings.openweather_api_key == VALID_ENV["OPENWEATHER_API_KEY"]
        assert settings.secret_key == "supersecretkey123"
        assert settings.algorithm == "HS256"
        assert settings.access_token_expire_minutes == 30


def test_settings_fail_missing_variables():
    """Verifies failure when required variables are missing."""
    env_missing_key = VALID_ENV.copy()
    del env_missing_key["OPENWEATHER_API_KEY"]

    with patch.dict(os.environ, env_missing_key, clear=True):
        with pytest.raises(ValidationError):
            Settings(_env_file=None) # type: ignore

    env_missing_db = VALID_ENV.copy()
    del env_missing_db["DATABASE_URL"]

    with patch.dict(os.environ, env_missing_db, clear=True):
        with pytest.raises(ValidationError):
            Settings(_env_file=None) # type: ignore


@pytest.mark.parametrize(
    "invalid_url",
    ["not_a_url", "http://", "postgres://user:pass@db"],
)
def test_settings_fail_invalid_database_url(invalid_url):
    """Verifies failure for invalid database URL formats.

    Args:
        invalid_url (str): The invalid URL string.
    """
    env_invalid = VALID_ENV.copy()
    env_invalid["DATABASE_URL"] = invalid_url

    with patch.dict(os.environ, env_invalid, clear=True):
        with pytest.raises(ValidationError):
            Settings(_env_file=None) # type: ignore


@pytest.mark.parametrize(
    "invalid_key",
    [
        "",
        "shortkey",
        "a1b2" * 10,
        "Z1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
        "!!b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
    ],
)
def test_settings_fail_invalid_api_key_format(invalid_key):
    """Verifies failure for invalid API key formats.

    Args:
        invalid_key (str): The invalid API key string.
    """
    env_invalid = VALID_ENV.copy()
    env_invalid["OPENWEATHER_API_KEY"] = invalid_key

    with patch.dict(os.environ, env_invalid, clear=True):
        with pytest.raises(ValidationError):
            Settings(_env_file=None) # type: ignore