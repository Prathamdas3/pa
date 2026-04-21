"""API v1 router aggregation.

Aggregates all v1 API routers into a single router for inclusion
in the main application.
"""

from fastapi import APIRouter
from app.api.v1.auth import auth_router
from app.api.v1.task import task_router
from app.api.v1.user import user_router
from app.core import get_logger

logger = get_logger(__name__)

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(task_router)
v1_router.include_router(user_router)

logger.info("V1 API routers registered: auth, tasks, users")
