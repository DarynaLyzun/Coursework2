"""Pydantic models for weather data validation.

This module defines the schemas used to structure and validate weather information
retrieved from external APIs (OpenWeatherMap). It ensures that the application
receives clean, typed data for AI processing.
"""

from pydantic import BaseModel, Field

class WeatherData(BaseModel):
    """Unified weather data structure for AI processing.

    This model normalizes the response from OpenWeatherMap into a clean
    structure that the NLI model can easily interpret.

    Attributes:
        description (str): Textual description (e.g., "scattered clouds").
        temperature (float): Current temperature in Celsius.
        feels_like (float): Human-perceived temperature in Celsius.
        wind_speed (float): Wind speed in meters/second.
        humidity (int): Relative humidity percentage (0-100).
        location (str): Name of the city or region.
    """
    description: str
    temperature: float
    feels_like: float
    wind_speed: float
    humidity: int = Field(ge=0, le=100, description="Humidity percentage")
    location: str