"""Recommendation API router.

This module defines the endpoints for generating clothing recommendations
based on real-time weather data and AI-powered description analysis.
"""

from fastapi import APIRouter, Request, Depends, HTTPException
import httpx
from app.services.weather_service import WeatherService
from app.core.utils import get_temperature_label, get_humidity_label, get_wind_label

CANDIDATE_LABELS = [
    "Rain",
    "Cold",
    "Hot",
    "Windy",
    "Freezing",
    "Warm",
    "Sunny",
    "Snow",
    "Stormy",
    "Mild",
    "Cool"
]

router = APIRouter()

def get_weather_service() -> WeatherService:
    """Dependency provider for the WeatherService.

    Returns:
        WeatherService: An instance of the service to fetch real-time weather.
    """
    return WeatherService()

@router.get("/recommend/{city}")
async def recommend(
    city: str,
    request: Request,
    weather_service: WeatherService = Depends(get_weather_service)
):
    """Generates a weather-based clothing recommendation for a specific city.

    Fetches the current weather and uses the NLI model (loaded in app.state)
    to classify the weather description against a set of clothing-relevant tags.

    Args:
        city (str): The name of the city to analyze.
        request (Request): The incoming request, used to access app.state.ai_service.
        weather_service (WeatherService): The service for fetching weather data.

    Returns:
        dict: A combined dictionary containing the weather data and the
            confidence scores for each label (e.g., Rain, Cold, Hot).

    Raises:
        HTTPException(404): If the city provided does not exist.
        HTTPException(503): If the AI Service is not initialized or unavailable.
        httpx.HTTPStatusError: For upstream weather API errors other than 404.
    """
    try:
        weather = await weather_service.get_current_weather(city=city)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"City '{city}' not found.")
        raise e

    ai = request.app.state.ai_service

    if ai is None:
        raise HTTPException(status_code=503, detail="AI Service is currently unavailable.")
    
    temp_label = get_temperature_label(weather.temperature)
    feels_label = get_temperature_label(weather.feels_like)
    humid_label = get_humidity_label(weather.humidity)
    wind_label = get_wind_label(weather.wind_speed)
    
    weather_description = (
        f"The weather is {weather.description}. "
        f"The temperature is {temp_label} and it feels {feels_label}. "
        f"It is {humid_label} and {wind_label}."
    )

    classification_result: dict = ai.classify_description(
        text=weather_description,
        candidate_labels=CANDIDATE_LABELS
    )
    
    filtered_result = {
        label: score 
        for label, score in classification_result.items() 
        if score >= 85
    }

    if not filtered_result:
        sorted_result = sorted(
            classification_result.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        filtered_result = dict(sorted_result[:2])

    return {"weather": weather} | filtered_result