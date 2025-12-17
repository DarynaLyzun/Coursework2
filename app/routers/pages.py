from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"hide_nav": True})

@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"active_page": "home"})

@router.get("/closet-view", response_class=HTMLResponse)
async def closet_page(request: Request):
    return templates.TemplateResponse(request=request, name="closet.html", context={"active_page": "closet"})