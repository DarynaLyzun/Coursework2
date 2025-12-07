"""Authentication API router.

This module defines the endpoints for user authentication and registration,
handling the creation of new user accounts via the API.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.crud.user_repo import create_user
from app.database.session import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user.

    Accepts user details, hashes the password (via the CRUD layer), and
    stores the new user in the database.

    Args:
        user_data (UserCreate): The user registration details (email, password).
        db (Session): The database session dependency.

    Returns:
        User: The created user object (password excluded by response_model).

    Raises:
        HTTPException(400): If the email is already registered.
    """
    try:
        new_user = create_user(db=db, user=user_data)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")