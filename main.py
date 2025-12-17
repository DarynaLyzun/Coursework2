"""Main entry point for the FastAPI application.

This module initializes the FastAPI app, sets up static files, templates,
and middleware (if any). It also defines the lifespan context for
startup and shutdown events.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import auth, pages, closet, recommendation
from app.services.ai_service import AIService
from app.services.weather_service import WeatherService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the application lifespan.

    Initializes global services (AI, Weather) on startup and cleans them up
    on shutdown.

    Args:
        app (FastAPI): The FastAPI application instance.
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
        RedirectResponse: A redirection to the '/dashboard' route.
    """
    return RedirectResponse(url="/dashboard")