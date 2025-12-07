"""CRUD operations for User management.

This module provides the database interactions for creating, retrieving,
and managing User accounts, handling password hashing securely.
"""

from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.database.models import User

def create_user(db: Session, user: UserCreate) -> User:
    """Creates a new user in the database.

    Hashes the plain password from the input schema and saves the user
    record with the secure hash.

    Args:
        db (Session): The database session.
        user (UserCreate): The user creation data (email and plain password).

    Returns:
        User: The created SQLAlchemy User object (with id and hashed_password).
    """
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user