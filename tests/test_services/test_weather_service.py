"""Unit tests for Weather service."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services.weather_service import WeatherService


@pytest.mark.asyncio
async def test_get_current_weather_success():
    """Verifies successful weather data fetching and mapping."""
    mock_data = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 20.5, "feels_like": 21.0, "humidity": 50},
        "wind": {"speed": 3.5},
        "name": "London",
    }

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_response.raise_for_status.return_value = None

        mock_client.get.return_value = mock_response

        service = WeatherService()
        result = await service.get_current_weather("London")

        assert result.description == "clear sky"
        assert result.temperature == 20.5
        assert result.location == "London"


@pytest.mark.asyncio
async def test_get_current_weather_not_found():
    """Verifies that a 404 error is raised for non-existent cities."""
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=MagicMock(), response=mock_response
        )

        mock_client.get.return_value = mock_response
        service = WeatherService()

        with pytest.raises(httpx.HTTPStatusError):
            await service.get_current_weather("Atlantis")


@pytest.mark.asyncio
async def test_get_current_weather_server_error():
    """Verifies that a 500 error is raised for server failures."""
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "500 Internal Server Error", request=MagicMock(), response=mock_response
        )

        mock_client.get.return_value = mock_response
        service = WeatherService()

        with pytest.raises(httpx.HTTPStatusError):
            await service.get_current_weather("London")


@pytest.mark.asyncio
async def test_get_current_weather_connection_error():
    """Verifies that connection errors are raised."""
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mock_client.get.side_effect = httpx.ConnectError(
            "Connection refused", request=MagicMock()
        )

        service = WeatherService()

        with pytest.raises(httpx.ConnectError):
            await service.get_current_weather("London")


@pytest.mark.asyncio
async def test_get_current_weather_malformed_data():
    """Verifies failure when response data is malformed."""
    malformed_data = {"weather": [], "name": "London"}

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mock_response = MagicMock()
        mock_response.json.return_value = malformed_data
        mock_response.raise_for_status.return_value = None

        mock_client.get.return_value = mock_response
        service = WeatherService()

        with pytest.raises((IndexError, KeyError)):
            await service.get_current_weather("London")