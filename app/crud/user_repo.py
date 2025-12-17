"""Data access operations for Users."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.database.models import User
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    """Creates a new user with a hashed password.

    Args:
        db (Session): The database session.
        user (UserCreate): The user creation schema.

    Returns:
        User: The created user instance.
    """
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
        email (str): The email address of the user.

    Returns:
        User | None: The user instance if found, otherwise None.
    """
    statement = select(User).where(User.email == email)
    user = db.scalar(statement)

    return user