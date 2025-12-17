"""Unit tests for API dependencies."""

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.crud.user_repo import create_user
from app.routers.auth import get_current_user
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_get_current_user_valid(db_session: Session):
    """Verifies that a valid token returns the correct user instance."""
    email = "valid_user@test.com"
    password = "StrongPassword1!"
    user_in = UserCreate(email=email, password=password)
    user = create_user(db_session, user_in)

    token = create_access_token(subject=email)

    current_user = await get_current_user(token=token, db=db_session)

    assert current_user.id == user.id
    assert current_user.email == email


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(db_session: Session):
    """Verifies that an invalid token raises an HTTPException."""
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token="invalid.token.string", db=db_session)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"


@pytest.mark.asyncio
async def test_get_current_user_user_not_found(db_session: Session):
    """Verifies that a token for a non-existent user raises an HTTPException."""
    token = create_access_token(subject="ghost@test.com")

    with pytest.raises(HTTPException) as exc:
        await get_current_user(token=token, db=db_session)

    assert exc.value.status_code == 401