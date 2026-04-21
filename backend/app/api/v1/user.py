from fastapi import APIRouter, status, Request, Depends, Response as HTTPResponse
from app.services import user_service_dep
from app.utils import verify_access_token
from app.core import AppException, get_logger
from app.schemas import Response, UserUpdate
from app.dependencies import require_admin, CurrentUser
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
async def get_current_user(req: Request, user_service: user_service_dep):
    token = req.cookies.get("access_jwt")
    if not token or not verify_access_token(token):
        logger.warning("Get current user: invalid or missing token")
        raise AppException("Not authenticated.", status_code=401)
    sub = verify_access_token(token)
    user_id_str = sub.get("id")
    try:
        user_id = UUID(user_id_str)
    except (ValueError, TypeError):
        raise AppException("Invalid user ID format", status_code=400)
    try:
        user = await user_service.get_user_by_id(user_id)
    except AppException as e:
        if e.status_code == 404:
            raise AppException("User not found.", status_code=401)
        raise
    logger.debug(f"Get current user: user_id={user_id}")
    return {
        "data": {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role,
        }
    }


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
    user_update: UserUpdate,
    user_service: user_service_dep,
    user_id: UUID = Depends(get_current_user_id),
):
    """Endpoint to update the authenticated user's username."""
    logger.info(
        f"Update user request: user_id={user_id}, new_username={user_update.username}"
    )
    await user_service.update_user(user_id, user_update.username)
    logger.info(f"User updated: user_id={user_id}")
    return {"data": {"message": " Username updated successfully."}}


@user_router.get("/admin/all", response_model=Response, status_code=status.HTTP_200_OK)
async def admin_get_all_users(
    user_service: user_service_dep, _: CurrentUser = Depends(require_admin)
):
    """Admin: get all registered users."""
    logger.info("Admin: fetching all users")
    users = await user_service.get_all_users()
    logger.info(f"Admin: retrieved {len(users)} users")
    return {
        "data": [
            {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "is_active": user.is_active,
            }
            for user in users
        ]
    }


@user_router.get(
    "/admin/{user_id}", response_model=Response, status_code=status.HTTP_200_OK
)
async def admin_get_user_by_id(
    user_id: UUID,
    user_service: user_service_dep,
    _: CurrentUser = Depends(require_admin),
):
    """Admin: get any user by ID."""
    logger.info(f"Admin: fetching user_id={user_id}")
    user = await user_service.get_user_by_id_admin(user_id)
    return {
        "data": {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role,
        }
    }


@user_router.delete(
    "/admin/{user_id}", response_model=Response, status_code=status.HTTP_200_OK
)
async def admin_delete_user(
    user_id: UUID,
    user_service: user_service_dep,
    _: CurrentUser = Depends(require_admin),
):
    """Admin: delete any user by ID."""
    logger.info(f"Admin: deleting user_id={user_id}")
    await user_service.delete_user_admin(user_id)
    return {"data": {"message": "User deleted by admin."}}


@user_router.patch(
    "/admin/{user_id}/role", response_model=Response, status_code=status.HTTP_200_OK
)
async def admin_update_role(
    user_id: UUID,
    role: str,
    user_service: user_service_dep,
    _: CurrentUser = Depends(require_admin),
):
    """Admin: promote or demote a user's role."""
    logger.info(f"Admin: updating role for user_id={user_id} to {role}")
    user = await user_service.update_user_role(user_id, role)
    return {
        "data": {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role,
        }
    }



