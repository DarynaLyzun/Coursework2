"""Pydantic schemas for authentication tokens."""

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for JWT access token response.

    Attributes:
        access_token (str): The encoded JWT access token.
        token_type (str): The type of token (e.g., 'bearer').
    """

    access_token: str
    token_type: str