"""Unit tests for security utilities.

This module verifies the password hashing, verification, and JWT token creation
functions to ensure the authentication layer is secure and functional.
"""

from jose import jwt
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings

def test_password_hashing():
    """Verifies that the password hashing function works correctly."""
    password = "securepassword"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert isinstance(hashed, str)
    assert verify_password(password, hashed)

def test_password_verification_failure():
    """Verifies that incorrect passwords return False."""
    password = "secretpassword"
    hashed = get_password_hash(password)
    
    assert not verify_password("wrongpassword", hashed)

def test_access_token_creation():
    """Verifies that a JWT token is correctly generated and signed.
    
    Ensures that:
    1. The token is a string.
    2. It can be decoded using the SECRET_KEY and Algorithm.
    3. The payload contains the correct subject (email) and an expiration.
    """
    email = "test@example.com"
    token = create_access_token(email)
    
    assert isinstance(token, str)
    
    payload = jwt.decode(
        token, 
        settings.secret_key, 
        algorithms=[settings.algorithm]
    )
    
    assert payload["sub"] == email
    assert "exp" in payload