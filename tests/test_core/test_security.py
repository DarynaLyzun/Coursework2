"""Unit tests for security utilities.

This module verifies the password hashing and verification functions
to ensure they are secure and functioning correctly with the Bcrypt scheme.
"""

from app.core.security import get_password_hash, verify_password

def test_password_hashing():
    """Verifies that the password hashing function works correctly.
    
    Ensures that:
    1. The hash is not the same as the plain password.
    2. The hash is a string.
    3. The hash can be verified against the original password.
    """
    password = "securepassword"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert isinstance(hashed, str)
    assert verify_password(password, hashed)

def test_password_verification_failure():
    """Verifies that incorrect passwords return False.
    
    Ensures that verification fails when the plain password does not
    match the hash.
    """
    password = "secretpassword"
    hashed = get_password_hash(password)
    
    assert not verify_password("wrongpassword", hashed)