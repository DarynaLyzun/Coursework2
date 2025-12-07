"""Integration tests for the main application entry point.

This module verifies that the FastAPI application starts up correctly,
initializes the necessary services (mocked), and handles the root endpoint.
"""

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi.routing import APIRoute
from main import app

def test_app_lifespan_and_root():
    """Verifies the startup/shutdown lifecycle and root endpoint.
    
    Ensures that:
    1. The AIService is initialized and stored in app.state on startup.
    2. The root endpoint returns a 200 OK response.
    3. Resources are cleaned up on shutdown.
    """
    with patch("main.AIService") as mock_service_cls:
        mock_instance = MagicMock()
        mock_service_cls.return_value = mock_instance

        with TestClient(app) as client:
            mock_service_cls.assert_called_once()
            
            assert app.state.ai_service == mock_instance
            
            response = client.get("/")
            assert response.status_code == 200
            assert response.json() == {"message": "Hello World"}

        assert app.state.ai_service is None
        
def test_router_is_included():
    """Verifies that the recommendation router is correctly registered."""
    route_paths = [
        route.path 
        for route in app.routes 
        if isinstance(route, APIRoute)
    ]
    
    assert "/recommend/{city}" in route_paths