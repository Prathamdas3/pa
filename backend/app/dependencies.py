from uuid import UUID
from fastapi import Depends, status, Request
from app.core import AppException
from app.models import UserRole
from app.utils import verify_access_token


class CurrentUser:
    def __init__(self, id: UUID, role: UserRole):
        self.id = id
        self.role = role


def get_current_user(req: Request) -> CurrentUser:
    token = req.cookies.get("access_jwt")
    if not token:
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, message="Unauthorized")
    
    payload = verify_access_token(token)
    if not payload:
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, message="Unauthorized")
    
    try:
        payload_id = payload.get("role")
        print(payload_id)
        return CurrentUser(id=UUID(payload.get("id")), role=payload.get("role"))
    except (ValueError, TypeError):
        raise AppException(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid user ID format")


def require_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if current_user.role != "admin":
        raise AppException(status_code=status.HTTP_403_FORBIDDEN, message="Admin access required")
    return current_user
