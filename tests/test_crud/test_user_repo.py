"""Unit tests for User CRUD operations.

This module verifies that the database repository functions correctly handle
data persistence and security transformations (like password hashing).
"""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.crud.user_repo import create_user, get_user_by_email
from app.schemas.user import UserCreate
from app.core.security import verify_password

def test_create_user(db_session: Session):
    """Verifies that a user can be created with a hashed password.
    
    Ensures that:
    1. The user is saved to the database.
    2. The email matches.
    3. The password stored is a hash, not the plain text.
    4. The hash is valid for the original password.
    """
    email = "newuser@example.com"
    password = "StrongPassword1!"
    user_in = UserCreate(email=email, password=password)

    user = create_user(db_session, user_in)

    assert user.email == email
    assert hasattr(user, "id")
    
    assert user.hashed_password != password
    assert verify_password(password, user.hashed_password)
    
def test_create_user_duplicate_email(db_session: Session):
    """Verifies that two users can't be created with the same email."""
    email = "newuser@example.com"
    password = "StrongPassword1!"
    user_one = UserCreate(email=email, password=password)
    user_two = UserCreate(email=email, password=password)

    user = create_user(db_session, user_one)
    with pytest.raises(IntegrityError):
        create_user(db_session, user_two)
        
def test_get_user_by_email_success(db_session: Session):
    """Verifies that an existing user can be retrieved by email."""
    email = "findme@test.com"
    password = "Password123!"
    user_in = UserCreate(email=email, password=password)
    create_user(db_session, user_in)

    user = get_user_by_email(db_session, email)

    assert user is not None
    assert user.email == email

def test_get_user_by_email_not_found(db_session: Session):
    """Verifies that searching for a non-existent email returns None."""
    user = get_user_by_email(db_session, "ghost@test.com")
    assert user is None