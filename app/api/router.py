from fastapi import APIRouter
from app.api.v1.router import v1_router
from app.core import get_logger

logger = get_logger(__name__)

api_router=APIRouter()

api_router.include_router(v1_router)

logger.info("API router initialized")