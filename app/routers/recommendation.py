"""API endpoints for generating clothing recommendations."""

from typing import Annotated, List, Sequence

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.utils import (
    CANDIDATE_LABELS,
    INCOMPATIBLE_KEYWORDS,
    get_humidity_label,
    get_temperature_label,
    get_wind_label,
)
from app.crud.tag_repo import get_items_by_tags
from app.database.models import Item, User
from app.database.session import get_db
from app.routers.auth import get_current_user
from app.services.weather_service import WeatherService

router = APIRouter()


def get_weather_service() -> WeatherService:
    """Dependency provider for the WeatherService.

    Returns:
        WeatherService: A new instance of the weather service.
    """
    return WeatherService()


def filter_incompatible_items(
    items: Sequence[Item], weather_tags: List[str]
) -> List[Item]:
    """Filters items that conflict with the current weather tags.

    Args:
        items (Sequence[Item]): The list of items to filter.
        weather_tags (List[str]): The active weather tags.

    Returns:
        List[Item]: A filtered list of suitable items.
    """
    filtered_items = []
    for item in items:
        desc = item.description.lower()
        is_bad = False
        for tag in weather_tags:
            if tag in INCOMPATIBLE_KEYWORDS:
                if any(k in desc for k in INCOMPATIBLE_KEYWORDS[tag]):
                    is_bad = True
                    break
            if is_bad:
                break
        if not is_bad:
            filtered_items.append(item)
    return filtered_items


@router.get("/recommend/{city}")
async def recommend(
    city: str,
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    weather_service: WeatherService = Depends(get_weather_service),
    db: Session = Depends(get_db),
):
    """Generates recommendations based on the current weather in a city.

    Args:
        city (str): The target city.
        request (Request): The request object containing application state.
        current_user (User): The authenticated user.
        weather_service (WeatherService): Service to fetch weather data.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing weather data, detected tags, and recommended items.

    Raises:
        HTTPException: If the city is not found or the AI service is unavailable.
    """
    try:
        weather = await weather_service.get_current_weather(city=city)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(404, detail=f"City '{city}' not found.")
        raise e

    ai = request.app.state.ai_service
    if not ai:
        raise HTTPException(503, detail="AI Service unavailable.")

    desc = (
        f"The weather is {weather.description}. "
        f"Temp is {get_temperature_label(weather.temperature)}. "
        f"{get_humidity_label(weather.humidity)} and {get_wind_label(weather.wind_speed)}."
    )

    results = ai.classify_description(
        desc,
        CANDIDATE_LABELS,
        hypothesis_template="The weather condition described is {}.",
    )

    filtered_tags = {l: s for l, s in results.items() if s >= 85}
    if not filtered_tags:
        filtered_tags = dict(
            sorted(results.items(), key=lambda x: x[1], reverse=True)[:2]
        )

    items = get_items_by_tags(db, current_user.id, list(filtered_tags))
    final_items = filter_incompatible_items(items, list(filtered_tags.keys()))

    return {"weather": weather, "tags": filtered_tags, "items": final_items}