"""
Dashboard endpoints for web interface
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()

# Setup Jinja2 templates
templates = Jinja2Templates(directory="api/templates")


@router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """
    Main dashboard page
    """
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "title": "Chakravyuh Brahmastra Dashboard"}
    )
