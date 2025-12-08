"""Main application entry point.

This module configures the FastAPI application, sets up the lifespan event handler
to manage heavy resources (like the AI model), and registers the API routers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.services.ai_service import AIService
from app.routers.recommendation import router as recommendation_router
from app.routers.auth import router as auth_router
from app.routers.closet import router as closet_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the startup and shutdown lifecycle of the application.

    Ensures that heavy resources, like the NLI classification model, are loaded
    into memory only once when the application starts and are available via
    app.state.
    """
    app.state.ai_service = AIService()
    
    yield
    
    app.state.ai_service = None

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(recommendation_router)
app.include_router(auth_router)
app.include_router(closet_router)

@app.get("/")
async def root():
    """Health check endpoint.

    Returns:
        dict: A simple greeting to verify the API is online.
    """
    return {"message": "Hello World"}