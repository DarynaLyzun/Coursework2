"""Security utilities for password hashing and verification.

This module uses Passlib with Bcrypt to handle secure password operations,
ensuring that raw passwords are never stored in the database.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hashes a plain password using Bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password string.
    """
    return pwd_context.hash(secret=password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a stored hash.

    Args:
        plain_password (str): The plain text password provided by the user.
        hashed_password (str): The hash stored in the database.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(secret=plain_password, hash=hashed_password)