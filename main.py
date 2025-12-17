"""Main application entry point and configuration."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import auth, closet, pages, recommendation
from app.services.ai_service import AIService
from app.services.weather_service import WeatherService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the lifecycle of application services.

    Args:
        app (FastAPI): The application instance.
    """
    app.state.ai_service = AIService()
    app.state.weather_service = WeatherService()
    yield
    app.state.ai_service = None
    app.state.weather_service = None


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(closet.router)
app.include_router(recommendation.router)


@app.get("/")
async def root():
    """Redirects the root URL to the dashboard.

    Returns:
        RedirectResponse: A redirect to the dashboard.
    """
    return RedirectResponse(url="/dashboard")