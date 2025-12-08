"""Authentication API router.

This module defines the endpoints for user authentication and registration,
handling the creation of new user accounts via the API.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.crud.user_repo import create_user, get_user_by_email
from app.database.session import get_db
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.database.models import User
from sqlalchemy.exc import IntegrityError

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    """Dependency that validates the JWT token and retrieves the current user.

    Args:
        token (str): The JWT token from the request header.
        db (Session): Database session.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException(401): If the token is invalid, expired, or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        email = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    return user

@router.post("/signup", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user."""
    try:
        new_user = create_user(db=db, user=user_data)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticates a user and issues a JWT access token."""
    user = get_user_by_email(db, form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}