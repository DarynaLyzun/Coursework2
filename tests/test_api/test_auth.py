"""Unit tests for the authentication router.

This module verifies the signup and login endpoints, ensuring that users can
register and authenticate to receive access tokens.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers import auth
from app.database.session import get_db
from app.crud.user_repo import create_user
from app.schemas.user import UserCreate

def setup_app(db_session):
    app = FastAPI()
    app.include_router(auth.router)
    app.dependency_overrides[get_db] = lambda: db_session
    return TestClient(app)

def test_signup_new_user(db_session):
    """Verifies that a new user can be registered via the API."""
    client = setup_app(db_session)
    payload = {"email": "api_user@test.com", "password": "StrongPassword1!"}
    
    response = client.post("/signup", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "api_user@test.com"
    assert "id" in data
    assert "password" not in data

def test_signup_duplicate_email(db_session):
    """Verifies that registering with an existing email returns a 400 error."""
    client = setup_app(db_session)
    payload = {"email": "duplicate@test.com", "password": "StrongPassword1!"}
    
    client.post("/signup", json=payload)
    
    response = client.post("/signup", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_access_token(db_session):
    """Verifies that a registered user can login and receive a JWT token.
    
    Ensures that:
    1. Valid credentials return a 200 OK.
    2. The response contains an 'access_token'.
    3. The token type is 'bearer'.
    """
    email = "login_test@example.com"
    password = "StrongPassword1!"
    user_in = UserCreate(email=email, password=password)
    create_user(db_session, user_in)

    client = setup_app(db_session)

    login_data = {
        "username": email,
        "password": password
    }
    
    response = client.post("/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_incorrect_password(db_session):
    """Verifies that login fails with wrong credentials."""
    email = "wrong_pass@example.com"
    password = "StrongPassword1!"
    user_in = UserCreate(email=email, password=password)
    create_user(db_session, user_in)

    client = setup_app(db_session)
    
    login_data = {"username": email, "password": "WrongPassword123!"}
    
    response = client.post("/login", data=login_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"