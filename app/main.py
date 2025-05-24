"""FastAPI application main module."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.v1.api import api_router

settings = get_settings()

setup_logging(settings.log_level)

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    description="A robust user management API built with FastAPI",
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    docs_url=f"{settings.api_v1_str}/docs",
    redoc_url=f"{settings.api_v1_str}/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request, exc):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/", tags=["health"])
async def root():
    """Root endpoint for health check."""
    return {
        "message": "User Management API",
        "version": settings.project_version,
        "status": "healthy",
        "environment": settings.environment,
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {
        "status": "healthy",
        "version": settings.project_version,
        "environment": settings.environment,
    }


app.include_router(api_router, prefix=settings.api_v1_str)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower(),
    )
