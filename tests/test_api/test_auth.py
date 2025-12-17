"""Integration tests for authentication endpoints."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.crud.user_repo import create_user
from app.database.session import get_db
from app.routers import auth
from app.schemas.user import UserCreate


def setup_app(db_session):
    """Configures a test FastAPI app with dependency overrides.

    Args:
        db_session: The database session fixture.

    Returns:
        TestClient: A configured test client.
    """
    app = FastAPI()
    app.include_router(auth.router)
    app.dependency_overrides[get_db] = lambda: db_session
    return TestClient(app)


def test_signup_new_user(db_session):
    """Verifies that a new user can successfully sign up."""
    client = setup_app(db_session)
    payload = {"email": "api_user@test.com", "password": "StrongPassword1!"}

    response = client.post("/signup", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "api_user@test.com"
    assert "id" in data
    assert "password" not in data


def test_signup_duplicate_email(db_session):
    """Verifies that signing up with a duplicate email fails."""
    client = setup_app(db_session)
    payload = {"email": "duplicate@test.com", "password": "StrongPassword1!"}

    client.post("/signup", json=payload)

    response = client.post("/signup", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_access_token(db_session):
    """Verifies that logging in with valid credentials returns a token."""
    email = "login_test@example.com"
    password = "StrongPassword1!"
    user_in = UserCreate(email=email, password=password)
    create_user(db_session, user_in)

    client = setup_app(db_session)

    login_data = {"username": email, "password": password}

    response = client.post("/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(db_session):
    """Verifies that logging in with incorrect credentials fails."""
    email = "wrong_pass@example.com"
    password = "StrongPassword1!"
    user_in = UserCreate(email=email, password=password)
    create_user(db_session, user_in)

    client = setup_app(db_session)

    login_data = {"username": email, "password": "WrongPassword123!"}

    response = client.post("/login", data=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"