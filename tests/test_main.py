"""Integration tests for application startup."""

from unittest.mock import MagicMock, patch

from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

from main import app


def test_app_lifespan_and_root():
    """Verifies lifecycle events and root endpoint."""
    with patch("main.AIService") as mock_service_cls:
        mock_instance = MagicMock()
        mock_service_cls.return_value = mock_instance

        with TestClient(app) as client:
            mock_service_cls.assert_called_once()

            assert app.state.ai_service == mock_instance

            response = client.get("/")
            assert response.status_code == 200

        assert app.state.ai_service is None


def test_router_is_included():
    """Verifies that routers are properly registered."""
    route_paths = [route.path for route in app.routes if isinstance(route, APIRoute)]

    assert "/recommend/{city}" in route_paths
    assert "/signup" in route_paths
    assert "/login" in route_paths
    assert "/closet/upload" in route_paths