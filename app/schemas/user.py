"""Pydantic models for user authentication and management.

This module defines the schemas used for creating new users (input) and
returning user details (output), ensuring that sensitive information like
passwords is handled securely and not exposed in API responses.
"""

import re
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator

class UserCreate(BaseModel):
    """Schema for user registration requests.

    Validates the input data required to create a new user account.

    Attributes:
        email (EmailStr): The user's valid email address.
        password (str): The raw password string (to be hashed before storage).
    """
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        """Enforces traditional password complexity rules."""
        
        # Rule 1: Must have an uppercase letter
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        
        # Rule 2: Must have a number
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
            
        # Rule 3: Must have a special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
            
        return value

class UserResponse(BaseModel):
    """Schema for user API responses.

    Defines the public user information returned to clients, strictly excluding
    sensitive data like password hashes.

    Attributes:
        id (int): The unique database identifier for the user.
        email (EmailStr): The user's email address.
    """
    id: int
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)