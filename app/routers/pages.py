"""API endpoints for serving HTML pages."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Serves the login page.

    Args:
        request (Request): The incoming request.

    Returns:
        HTMLResponse: The rendered login HTML.
    """
    return templates.TemplateResponse(
        request=request, name="login.html", context={"hide_nav": True}
    )


@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Serves the main dashboard page.

    Args:
        request (Request): The incoming request.

    Returns:
        HTMLResponse: The rendered dashboard HTML.
    """
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"active_page": "home"}
    )


@router.get("/closet-view", response_class=HTMLResponse)
async def closet_page(request: Request):
    """Serves the closet management page.

    Args:
        request (Request): The incoming request.

    Returns:
        HTMLResponse: The rendered closet HTML.
    """
    return templates.TemplateResponse(
        request=request, name="closet.html", context={"active_page": "closet"}
    )