"""Pydantic schemas for weather data validation."""

from pydantic import BaseModel


class WeatherData(BaseModel):
    """Normalized weather data structure.

    Attributes:
        description (str): Text description of the weather.
        temperature (float): Current temperature.
        feels_like (float): Human-perceived temperature.
        wind_speed (float): Wind speed.
        humidity (int): Relative humidity percentage.
        location (str): Name of the location.
    """

    description: str
    temperature: float
    feels_like: float
    wind_speed: float
    humidity: int
    location: str