"""Unit tests for security utilities."""

from jose import jwt

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password


def test_password_hashing():
    """Verifies successful password hashing."""
    password = "securepassword"
    hashed = get_password_hash(password)

    assert hashed != password
    assert isinstance(hashed, str)
    assert verify_password(password, hashed)


def test_password_verification_failure():
    """Verifies that incorrect passwords fail validation."""
    password = "secretpassword"
    hashed = get_password_hash(password)

    assert not verify_password("wrongpassword", hashed)


def test_access_token_creation():
    """Verifies correct JWT token creation."""
    email = "test@example.com"
    token = create_access_token(email)

    assert isinstance(token, str)

    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

    assert payload["sub"] == email
    assert "exp" in payload