"""Integration tests for recommendation endpoints."""

from unittest.mock import AsyncMock, MagicMock

import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database.models import ClothingWeather, Item, User, WeatherTag
from app.database.session import get_db
from app.routers import recommendation
from app.routers.auth import get_current_user
from app.schemas.weather import WeatherData


def test_recommend_endpoint(db_session: Session):
    """Verifies successful recommendation generation flow."""
    user = User(email="rec_test@example.com", hashed_password="pw")
    db_session.add(user)
    db_session.commit()

    coat = Item(description="Heavy Raincoat", owner=user)
    db_session.add(coat)
    db_session.commit()

    tag = WeatherTag(name="Rain")
    db_session.add(tag)
    db_session.commit()

    link = ClothingWeather(item=coat, tag=tag, confidence=99)
    db_session.add(link)
    db_session.commit()

    app = FastAPI()
    app.include_router(recommendation.router)

    mock_weather_service = AsyncMock()
    mock_weather = WeatherData(
        description="rainy",
        temperature=15.0,
        feels_like=12.0,
        wind_speed=10.0,
        humidity=80,
        location="London",
    )
    mock_weather_service.get_current_weather.return_value = mock_weather

    mock_ai = MagicMock()
    mock_ai.classify_description.return_value = {"Rain": 95, "Cold": 10}

    app.state.ai_service = mock_ai
    app.dependency_overrides[recommendation.get_weather_service] = (
        lambda: mock_weather_service
    )
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: user

    client = TestClient(app)
    response = client.get("/recommend/London")

    assert response.status_code == 200
    data = response.json()
    assert data["weather"]["description"] == "rainy"
    assert data["tags"]["Rain"] == 95
    assert len(data["items"]) == 1
    assert data["items"][0]["description"] == "Heavy Raincoat"


def test_recommend_city_not_found(db_session: Session):
    """Verifies that a non-existent city returns a 404 error."""
    app = FastAPI()
    app.include_router(recommendation.router)

    user = User(email="error_test@example.com", hashed_password="pw")
    db_session.add(user)
    db_session.commit()

    mock_weather_service = AsyncMock()
    mock_weather_service.get_current_weather.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=MagicMock(), response=MagicMock(status_code=404)
    )

    app.dependency_overrides[recommendation.get_weather_service] = (
        lambda: mock_weather_service
    )
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: user

    client = TestClient(app)
    response = client.get("/recommend/Atlantis")

    assert response.status_code == 404
    assert response.json()["detail"] == "City 'Atlantis' not found."


def test_recommend_ai_service_unavailable(db_session: Session):
    """Verifies that unavailable AI service returns a 503 error."""
    app = FastAPI()
    app.include_router(recommendation.router)

    user = User(email="ai_fail_test@example.com", hashed_password="pw")
    db_session.add(user)
    db_session.commit()

    mock_weather_service = AsyncMock()
    mock_weather_service.get_current_weather.return_value = WeatherData(
        description="test",
        temperature=0,
        feels_like=0,
        wind_speed=0,
        humidity=0,
        location="Test",
    )
    app.dependency_overrides[recommendation.get_weather_service] = (
        lambda: mock_weather_service
    )
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: user

    app.state.ai_service = None

    client = TestClient(app)
    response = client.get("/recommend/London")

    assert response.status_code == 503
    assert response.json()["detail"] == "AI Service unavailable."