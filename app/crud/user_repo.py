"""CRUD operations for User management.

This module provides the database interactions for creating, retrieving,
and managing User accounts, handling password hashing securely.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.database.models import User

def create_user(db: Session, user: UserCreate) -> User:
    """Creates a new user in the database."""
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def get_user_by_email(db: Session, email: str) -> User | None:
    """Retrieves a user by their email address.

    Args:
        db (Session): The database session.
        email (str): The email address to search for.

    Returns:
        User | None: The user object if found, otherwise None.
    """
    statement = select(User).where(User.email == email)
    user = db.scalar(statement)
    
    return user