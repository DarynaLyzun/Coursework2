"""Unit tests for the WeatherService.

This module verifies the behavior of the WeatherService, ensuring it correctly
interacts with the OpenWeatherMap API settings and handles various network
and data scenarios using mocks.
"""

import pytest
import httpx
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.weather_service import WeatherService

@pytest.mark.asyncio
async def test_get_current_weather_success():
    """Verifies that valid weather data is correctly fetched and mapped.
    
    Ensures that when the API returns a standard 200 OK response, the service
    correctly parses the JSON and populates the WeatherData model.
    """
    mock_data = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 20.5, "feels_like": 21.0, "humidity": 50},
        "wind": {"speed": 3.5},
        "name": "London"
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
    """Verifies that a 404 error (City Not Found) raises an HTTPStatusError.
    
    Simulates a scenario where the user requests a non-existent city,
    expecting the service to bubble up the HTTP error.
    """
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
    """Verifies that a 500 error (Server Error) raises an HTTPStatusError.
    
    Simulates an internal error at OpenWeatherMap to ensure the application
    does not crash silently.
    """
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
    """Verifies that network connectivity issues raise a ConnectError.
    
    Simulates a scenario where the API server is unreachable (e.g., DNS failure
    or offline status) by making the client.get call itself fail.
    """
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mock_client.get.side_effect = httpx.ConnectError("Connection refused", request=MagicMock())

        service = WeatherService()

        with pytest.raises(httpx.ConnectError):
            await service.get_current_weather("London")

@pytest.mark.asyncio
async def test_get_current_weather_malformed_data():
    """Verifies that the service fails if required keys are missing from the response.
    
    Ensures that if the API returns a 200 OK but with unexpected JSON structure
    (e.g., missing 'weather' list), the service raises an appropriate error.
    """
    malformed_data = {"weather": [], "name": "London"} # Missing 'main', empty 'weather'

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