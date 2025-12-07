"""Unit tests for User schemas.

This module verifies that the Pydantic models correctly validate input data,
specifically enforcing the custom password complexity rules defined in
the UserCreate schema.
"""

import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate

def test_user_create_valid_password():
    """Verifies that a password meeting all complexity requirements is accepted."""
    valid_password = "StrongPassword1!"
    user = UserCreate(email="test@example.com", password=valid_password)
    assert user.password == valid_password

@pytest.mark.parametrize("password", [
    "short1!",        # Too short (<8 chars)
    "nouppercase1!",  # Missing uppercase
    "NO_DIGIT!",      # Missing digit
    "NoSymbol123",    # Missing special character
])
def test_user_create_invalid_passwords(password):
    """Verifies that passwords violating complexity rules raise ValidationError.
    
    Ensures that the custom validator and Field constraints correctly reject
    passwords that are too short or lack required character types.
    """
    with pytest.raises(ValidationError):
        UserCreate(email="test@example.com", password=password)