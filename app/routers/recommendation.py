"""Recommendation API router.

This module defines the endpoints for generating clothing recommendations
based on real-time weather data and AI-powered description analysis.
"""

from fastapi import APIRouter, Request, Depends, HTTPException
import httpx
from app.services.weather_service import WeatherService

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

    candidate_labels = [
        "Rain",
        "Cold",
        "Hot",
        "Windy",
        "Freezing",
        "Warm"
    ]

    classification_result: dict = ai.classify_description(
        text=weather.description,
        candidate_labels=candidate_labels
    )

    return {"weather": weather} | classification_result