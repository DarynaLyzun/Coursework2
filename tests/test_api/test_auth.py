"""Unit tests for the authentication router.

This module verifies the signup endpoint, ensuring that users can be
registered and that duplicate emails are handled correctly.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers import auth
from app.database.session import get_db

def test_signup_new_user(db_session):
    """Verifies that a new user can be registered via the API."""
    app = FastAPI()
    app.include_router(auth.router)
    
    app.dependency_overrides[get_db] = lambda: db_session
    
    client = TestClient(app)
    
    payload = {"email": "api_user@test.com", "password": "StrongPassword1!"}
    response = client.post("/signup", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "api_user@test.com"
    assert "id" in data
    assert "password" not in data

def test_signup_duplicate_email(db_session):
    """Verifies that registering with an existing email returns a 400 error."""
    app = FastAPI()
    app.include_router(auth.router)
    app.dependency_overrides[get_db] = lambda: db_session
    client = TestClient(app)
    
    payload = {"email": "duplicate@test.com", "password": "StrongPassword1!"}
    
    client.post("/signup", json=payload)
    
    response = client.post("/signup", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"