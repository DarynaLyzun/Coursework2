"""Pydantic schemas for User data validation."""

import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """Schema for user creation and registration.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password (min 8 chars, max 72).
    """

    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        """Validates that the password meets complexity requirements.

        Args:
            value (str): The password string.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password lacks uppercase letters, digits, or special characters.
        """
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")

        return value


class UserResponse(BaseModel):
    """Schema for user public data response.

    Attributes:
        id (int): The user's unique ID.
        email (EmailStr): The user's email address.
    """

    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)