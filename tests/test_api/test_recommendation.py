"""Unit tests for the recommendation router.

This module verifies the /recommend endpoint in isolation by mocking
both the external weather service and the internal AI service. It covers
success scenarios as well as error handling for missing cities and services.
"""

from unittest.mock import AsyncMock, MagicMock
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers import recommendation
from app.schemas.weather import WeatherData

def test_recommend_endpoint():
    """Verifies that the recommendation endpoint correctly orchestrates services.

    Ensures that:
    1. Weather data is fetched (via dependency override).
    2. AI classification is performed (via app.state mock).
    3. The response combines both results into a single dictionary.
    """
    app = FastAPI()
    app.include_router(recommendation.router)

    mock_weather_service = AsyncMock()
    mock_weather = WeatherData(
        description="rainy",
        temperature=15.0,
        feels_like=12.0,
        wind_speed=10.0,
        humidity=80,
        location="London"
    )
    mock_weather_service.get_current_weather.return_value = mock_weather

    mock_ai = MagicMock()
    mock_ai.classify_description.return_value = {"Rain": 95, "Cold": 10}

    app.state.ai_service = mock_ai
    app.dependency_overrides[recommendation.get_weather_service] = lambda: mock_weather_service

    client = TestClient(app)
    response = client.get("/recommend/London")

    assert response.status_code == 200
    data = response.json()
    assert data["weather"]["description"] == "rainy"
    assert data["Rain"] == 95

def test_recommend_city_not_found():
    """Verifies that a 404 from the weather service is passed through to the user.

    Simulates an upstream 404 error (City Not Found) and ensures the API
    transforms this into a user-friendly 404 HTTPException.
    """
    app = FastAPI()
    app.include_router(recommendation.router)

    mock_weather_service = AsyncMock()
    mock_weather_service.get_current_weather.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=MagicMock(), response=MagicMock(status_code=404)
    )

    app.dependency_overrides[recommendation.get_weather_service] = lambda: mock_weather_service

    client = TestClient(app)
    response = client.get("/recommend/Atlantis")

    assert response.status_code == 404
    assert response.json()["detail"] == "City 'Atlantis' not found."

def test_recommend_ai_service_unavailable():
    """Verifies that the endpoint returns a 503 error if the AI service is missing.

    Simulates a scenario where app.state.ai_service is None (e.g., initialization
    failure) and ensures the API returns a 503 Service Unavailable response
    instead of crashing with a 500 error.
    """
    app = FastAPI()
    app.include_router(recommendation.router)

    mock_weather_service = AsyncMock()
    mock_weather_service.get_current_weather.return_value = WeatherData(
        description="test", temperature=0, feels_like=0, wind_speed=0, humidity=0, location="Test"
    )
    app.dependency_overrides[recommendation.get_weather_service] = lambda: mock_weather_service

    app.state.ai_service = None

    client = TestClient(app)
    response = client.get("/recommend/London")

    assert response.status_code == 503
    assert response.json()["detail"] == "AI Service is currently unavailable."