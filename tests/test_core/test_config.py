"""Unit tests for application configuration.

This module verifies that the Settings class correctly validates environment
variables, ensuring that the application fails fast if the configuration is
missing, invalid, or insecure.
"""

import os
from unittest.mock import patch
import pytest
from pydantic import ValidationError
from app.core.config import Settings

# --- Fixtures & Constants ---

VALID_ENV = {
    "DATABASE_URL": "mariadb+mariadbconnector://user:pass@localhost:3306/test_db",
    "OPENWEATHER_API_KEY": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
    "SECRET_KEY": "supersecretkey123"
}

# --- Happy Path Tests ---

def test_settings_load_correctly():
    """Verifies that settings load correctly when the environment is valid.
    
    Ensures that valid connection strings and API keys are accepted and
    accessible via the Settings instance.
    """
    with patch.dict(os.environ, VALID_ENV, clear=True):
        settings = Settings(_env_file=None)  # type: ignore
        
        assert str(settings.database_url) == VALID_ENV["DATABASE_URL"]
        assert settings.openweather_api_key == VALID_ENV["OPENWEATHER_API_KEY"]
        assert settings.secret_key == "supersecretkey123"
        assert settings.algorithm == "HS256"
        assert settings.access_token_expire_minutes == 30

# --- Missing Variable Tests ---

def test_settings_fail_missing_variables():
    """Verifies that a ValidationError is raised if variables are missing.
    
    Checks that the application refuses to start if either the DATABASE_URL
    or the OPENWEATHER_API_KEY is absent from the environment.
    """
    # Case 1: Missing API Key
    env_missing_key = VALID_ENV.copy()
    del env_missing_key["OPENWEATHER_API_KEY"]
    
    with patch.dict(os.environ, env_missing_key, clear=True):
        with pytest.raises(ValidationError):
            Settings(_env_file=None) # type: ignore

    # Case 2: Missing Database URL
    env_missing_db = VALID_ENV.copy()
    del env_missing_db["DATABASE_URL"]
    
    with patch.dict(os.environ, env_missing_db, clear=True):
        with pytest.raises(ValidationError):
            Settings(_env_file=None) # type: ignore

# --- Invalid Format Tests ---

@pytest.mark.parametrize("invalid_url", [
    "not_a_url",              # No scheme
    "http://",                # Missing host
    "postgres://user:pass@db" # Wrong scheme (expects mariadb)
])
def test_settings_fail_invalid_database_url(invalid_url):
    """Verifies that invalid database URLs raise a ValidationError.
    
    Args:
        invalid_url (str): A malformed or incorrect connection string.
    """
    env_invalid = VALID_ENV.copy()
    env_invalid["DATABASE_URL"] = invalid_url
    
    with patch.dict(os.environ, env_invalid, clear=True):
        with pytest.raises(ValidationError):
            Settings(_env_file=None) # type: ignore

@pytest.mark.parametrize("invalid_key", [
    "",                                  # Empty string
    "shortkey",                          # Too short (<32)
    "a1b2" * 10,                         # Too long (>32)
    "Z1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",  # Invalid char ('Z' is not hex)
    "!!b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",  # Special characters
])
def test_settings_fail_invalid_api_key_format(invalid_key):
    """Verifies that the API key regex enforces correct formatting.
    
    Ensures that keys are exactly 32 characters long and contain only
    hexadecimal characters (0-9, a-f).

    Args:
        invalid_key (str): A malformed API key to test.
    """
    env_invalid = VALID_ENV.copy()
    env_invalid["OPENWEATHER_API_KEY"] = invalid_key
    
    with patch.dict(os.environ, env_invalid, clear=True):
        with pytest.raises(ValidationError):
            Settings(_env_file=None) # type: ignore