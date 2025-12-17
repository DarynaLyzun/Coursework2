"""Recommendation API router."""
from typing import Annotated, List, Sequence
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends, HTTPException
import httpx

from app.database.session import get_db
from app.database.models import User, Item
from app.services.weather_service import WeatherService
from app.core.utils import get_temperature_label, get_humidity_label, get_wind_label, CANDIDATE_LABELS, INCOMPATIBLE_KEYWORDS
from app.routers.auth import get_current_user
from app.crud.tag_repo import get_items_by_tags

router = APIRouter()

def get_weather_service() -> WeatherService:
    return WeatherService()

def filter_incompatible_items(items: Sequence[Item], weather_tags: List[str]) -> List[Item]:
    """Filters out items whose description conflicts with the active weather tags."""
    filtered_items = []
    for item in items:
        desc = item.description.lower()
        is_bad = False
        for tag in weather_tags:
            if tag in INCOMPATIBLE_KEYWORDS:
                if any(k in desc for k in INCOMPATIBLE_KEYWORDS[tag]):
                    is_bad = True
                    break
            if is_bad: break
        if not is_bad: filtered_items.append(item)
    return filtered_items

@router.get("/recommend/{city}")
async def recommend(
    city: str,
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    weather_service: WeatherService = Depends(get_weather_service),
    db: Session = Depends(get_db)
):
    """Generates a weather-based clothing recommendation for a specific city.

    Fetches the current weather and uses the NLI model (loaded in app.state)
    to classify the weather description against a set of clothing-relevant tags.

    Args:
        city (str): The name of the city to analyze.
        request (Request): The incoming request, used to access app.state.ai_service.
        current_user (User): The authenticated user asking for a recommendation.
        weather_service (WeatherService): The service for fetching weather data.
        db (Session): Database session.

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
        if e.response.status_code == 404: raise HTTPException(404, detail=f"City '{city}' not found.")
        raise e

    ai = request.app.state.ai_service
    if not ai: raise HTTPException(503, detail="AI Service unavailable.")
    
    desc = f"The weather is {weather.description}. Temp is {get_temperature_label(weather.temperature)}. {get_humidity_label(weather.humidity)} and {get_wind_label(weather.wind_speed)}."

    results = ai.classify_description(desc, CANDIDATE_LABELS, hypothesis_template="The weather condition described is {}.")
    
    filtered_tags = {l: s for l, s in results.items() if s >= 85}
    if not filtered_tags:
        filtered_tags = dict(sorted(results.items(), key=lambda x: x[1], reverse=True)[:2])
        
    items = get_items_by_tags(db, current_user.id, list(filtered_tags))
    final_items = filter_incompatible_items(items, list(filtered_tags.keys()))

    return {"weather": weather, "tags": filtered_tags, "items": final_items}