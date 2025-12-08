"""Pydantic models for authentication tokens.

This module defines the schema for the JWT access token response, ensuring
that clients receive a consistent structure containing the token string
and its type (e.g., 'bearer').
"""

from pydantic import BaseModel

class Token(BaseModel):
    """Schema for the JWT access token response.

    Attributes:
        access_token (str): The encoded JWT string.
        token_type (str): The type of token (usually "bearer").
    """
    access_token: str
    token_type: str