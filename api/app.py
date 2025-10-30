"""
Chakravyuh-Brahmastra REST API
FastAPI application with async support
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from config.settings import settings
from common.logger import logger
from api.routes import scan, dashboard


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown"""
    # Startup
    logger.info("application_startup", version=settings.APP_VERSION)
    yield
    # Shutdown
    logger.info("application_shutdown")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Cyber Defense Framework",
    lifespan=lifespan
)

# CORS middleware (for web dashboard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scan.router, prefix=f"{settings.API_PREFIX}/scan", tags=["Scanning"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# Mount static files (for web assets)
# app.mount("/static", StaticFiles(directory="api/static"), name="static")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "endpoints": {
            "api_docs": "/docs",
            "dashboard": "/dashboard",
            "scan": f"{settings.API_PREFIX}/scan"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    uvicorn.run(
        "api.app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
