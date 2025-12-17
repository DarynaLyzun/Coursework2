"""Unit tests for User repository operations."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.crud.user_repo import create_user, get_user_by_email
from app.schemas.user import UserCreate


def test_create_user(db_session: Session):
    """Verifies user creation and password hashing."""
    email = "newuser@example.com"
    password = "StrongPassword1!"
    user_in = UserCreate(email=email, password=password)

    user = create_user(db_session, user_in)

    assert user.email == email
    assert hasattr(user, "id")

    assert user.hashed_password != password
    assert verify_password(password, user.hashed_password)


def test_create_user_duplicate_email(db_session: Session):
    """Verifies that duplicate email creation fails."""
    email = "newuser@example.com"
    password = "StrongPassword1!"
    user_one = UserCreate(email=email, password=password)
    user_two = UserCreate(email=email, password=password)

    create_user(db_session, user_one)
    with pytest.raises(IntegrityError):
        create_user(db_session, user_two)


def test_get_user_by_email_success(db_session: Session):
    """Verifies retrieval of an existing user by email."""
    email = "findme@test.com"
    password = "Password123!"
    user_in = UserCreate(email=email, password=password)
    create_user(db_session, user_in)

    user = get_user_by_email(db_session, email)

    assert user is not None
    assert user.email == email


def test_get_user_by_email_not_found(db_session: Session):
    """Verifies that non-existent users return None."""
    user = get_user_by_email(db_session, "ghost@test.com")
    assert user is None