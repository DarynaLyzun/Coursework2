"""Integration tests for HTML page endpoints."""

from fastapi.testclient import TestClient

from main import app


def test_login_page_loads():
    """Verifies that the login page loads successfully with a 200 OK status."""
    client = TestClient(app)
    response = client.get("/login")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Login" in response.text


def test_dashboard_page_loads():
    """Verifies that the dashboard page loads successfully."""
    client = TestClient(app)
    response = client.get("/")
    
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_closet_page_loads():
    """Verifies that the closet view page loads successfully."""
    client = TestClient(app)
    response = client.get("/closet-view")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]