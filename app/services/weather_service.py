"""Service for interacting with the OpenWeatherMap API.

This module handles the external communication with weather providers,
fetching real-time data and normalizing it into the application's
schema formats.
"""

import httpx
from app.core.config import settings
from app.schemas.weather import WeatherData

class WeatherService:
    """Handles communication with the OpenWeatherMap API.

    Attributes:
        BASE_URL (str): The endpoint for the current weather data.
    """
    BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"

    async def get_current_weather(self, city: str) -> WeatherData:
        """Fetches and normalizes current weather data for a specific city.

        Args:
            city (str): The name of the city to look up (e.g., "London").

        Returns:
            WeatherData: A validated object containing description, temperature,
                and other atmospheric metrics.

        Raises:
            httpx.HTTPStatusError: If the API returns a 4xx or 5xx error
                (e.g., city not found or invalid API key).
        """
        params = {
            "q": city,
            "appid": settings.openweather_api_key,
            "units": "metric"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url=self.BASE_URL, params=params)
            
            response.raise_for_status()
            data = response.json()

            return WeatherData(
                description=data["weather"][0]["description"],
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                wind_speed=data["wind"]["speed"],
                humidity=data["main"]["humidity"],
                location=data["name"]
            )