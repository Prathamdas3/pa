from fastapi import APIRouter, status, Request, Depends, Response as HTTPResponse
from app.services import user_service_dep
from app.utils import verify_access_token
from app.core import AppException, get_logger
from app.schemas import Response
from uuid import UUID

logger = get_logger(__name__)

user_router = APIRouter(prefix="/users", tags=["users"])


def get_current_user_id(req: Request) -> UUID:
    """Dependency to extract and verify JWT from cookies, returning the user ID."""
    token = req.cookies.get("access_jwt")
    if not token:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Unauthorized"
        )
    payload = verify_access_token(token)
    if not payload:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Unauthorized"
        )
    id = payload.get("id")
    try:
        return UUID(id)
    except ValueError:
        raise AppException(
            status_code=status.HTTP_400_BAD_REQUEST, message="Invalid user ID format"
        )


@user_router.get("/me", response_model=Response, status_code=status.HTTP_200_OK)
async def get_current_user(req: Request):
    token = req.cookies.get("access_jwt")
    if not token or not verify_access_token(token):
        logger.warning("Get current user: invalid or missing token")
        raise AppException("Not authenticated.", status_code=401)
    sub = verify_access_token(token)
    logger.debug(f"Get current user: user_id={sub.get('id')}")
    return {"data": {**sub}}


@user_router.delete("/me", status_code=status.HTTP_200_OK, response_model=Response)
async def delete_current_user(
    res: HTTPResponse,
    user_service: user_service_dep,
    user_id: UUID = Depends(get_current_user_id),
):
    """Endpoint to delete the authenticated user."""
    logger.info(f"Delete user request: user_id={user_id}")
    await user_service.delete_user(user_id)
    logger.info(f"User deleted: user_id={user_id}")
    res.delete_cookie("access_jwt")
    return {"data": {"message": "User deleted successfully."}}


@user_router.patch("/me", status_code=status.HTTP_200_OK, response_model=Response)
async def update_current_user(
    username: str,
    user_service: user_service_dep,
    user_id: UUID = Depends(get_current_user_id),
):
    """Endpoint to update the authenticated user's username."""
    logger.info(f"Update user request: user_id={user_id}, new_username={username}")
    user = await user_service.update_user(user_id, username)
    logger.info(f"User updated: user_id={user_id}")
    return {"data": user}
