"""Service for interacting with the OpenWeatherMap API."""

import httpx

from app.core.config import settings
from app.schemas.weather import WeatherData


class WeatherService:
    """Handles fetching and processing weather data.

    Attributes:
        BASE_URL (str): The OpenWeatherMap API endpoint.
    """

    BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"

    async def get_current_weather(self, city: str) -> WeatherData:
        """Fetches current weather data for a specific city.

        Args:
            city (str): The name of the city.

        Returns:
            WeatherData: The normalized weather data.

        Raises:
            httpx.HTTPStatusError: If the API request fails.
        """
        params = {
            "q": city,
            "appid": settings.openweather_api_key,
            "units": "metric",
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
                location=data["name"],
            )