"""Security utilities for password management and token generation."""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Generates a Bcrypt hash for a given password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password string.
    """
    return pwd_context.hash(secret=password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The stored hashed password.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def create_access_token(subject: str) -> str:
    """Creates a JWT access token for a subject.

    Args:
        subject (str): The subject (identity) for the token, typically an email.

    Returns:
        str: The encoded JWT access token string.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode = {"exp": expire, "sub": str(subject)}

    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )

    return encoded_jwt