"""Unit tests for user schema validation."""

import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate


def test_user_create_valid_password():
    """Verifies that a valid password passes validation."""
    valid_password = "StrongPassword1!"
    user = UserCreate(email="test@example.com", password=valid_password)
    assert user.password == valid_password


@pytest.mark.parametrize(
    "password",
    [
        "short1!",
        "nouppercase1!",
        "NO_DIGIT!",
        "NoSymbol123",
    ],
)
def test_user_create_invalid_passwords(password):
    """Verifies that invalid passwords fail validation."""
    with pytest.raises(ValidationError):
        UserCreate(email="test@example.com", password=password)