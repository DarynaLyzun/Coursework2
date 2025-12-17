"""API endpoints for user authentication and registration."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.crud.user_repo import create_user, get_user_by_email
from app.database.models import User
from app.database.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Dependency to retrieve the currently authenticated user from a JWT token.

    Args:
        token (str): The JWT access token.
        db (Session): The database session.

    Returns:
        User: The authenticated user instance.

    Raises:
        HTTPException: If the token is invalid, expired, or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
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
    """Registers a new user in the system.

    Args:
        user_data (UserCreate): The user registration data.
        db (Session): The database session.

    Returns:
        UserResponse: The created user details.

    Raises:
        HTTPException: If the email address is already registered.
    """
    try:
        new_user = create_user(db=db, user=user_data)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Authenticates a user and issues an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The login credentials (username/password).
        db (Session): The database session.

    Returns:
        Token: The JWT access token.

    Raises:
        HTTPException: If authentication fails.
    """
    user = get_user_by_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}