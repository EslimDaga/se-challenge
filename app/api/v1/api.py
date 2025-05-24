"""API v1 router aggregation."""

from fastapi import APIRouter
from app.api.v1.routes import user

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
