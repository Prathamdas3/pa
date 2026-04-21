"""API v1 router aggregation.

Aggregates all v1 API routers into a single router for inclusion
in the main application.
"""

from fastapi import APIRouter
from app.api.v1.auth import auth_router
from app.api.v1.task import task_router
from app.api.v1.user import user_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(task_router)
v1_router.include_router(user_router)
