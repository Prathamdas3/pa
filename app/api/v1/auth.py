from fastapi import APIRouter, Response as HTTPResponse, status, Request
from app.services import user_service_dep
from app.schemas import Response, UserCreate, LoginUser
from app.models import UserRole
from app.utils import create_access_token, verify_password, verify_access_token
from app.core import config, AppException

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def set_cookies(res:HTTPResponse, access_token:str):
    res.set_cookie(
        key="access_jwt",
        httponly=True,
        value=access_token,
        samesite="lax",
        secure=config.env == "production",
        max_age=config.access_token_expire_minutes * 60,
    )


@auth_router.post(
    "/sign-up/user", status_code=status.HTTP_201_CREATED, response_model=Response
)
async def sign_up_user(
    res: HTTPResponse, user: UserCreate, user_service: user_service_dep
):
    """Endpoint for user registration."""
    created_user = await user_service.create_user(user, UserRole.user)
    access_token = create_access_token(
        {
            "sub": {
                "id": created_user.id,
                "email": created_user.email,
                "username": created_user.username,
                "role": created_user.role,
            }
        },
    )
    set_cookies(res, access_token)
    return {
        "data": {
            "id": created_user.id,
            "email": created_user.email,
            "username": created_user.username,
        }
    }


@auth_router.post(
    "/sign-up/admin", status_code=status.HTTP_201_CREATED, response_model=Response
)
async def sign_up_admin(
    res: HTTPResponse, user: UserCreate, user_service: user_service_dep
):
    """Endpoint for user registration."""
    created_user = await user_service.create_user(user, UserRole.admin)
    access_token = create_access_token(
        {
            "sub": {
                "id": created_user.id,
                "email": created_user.email,
                "username": created_user.username,
                "role": created_user.role,
            }
        },
    )
    set_cookies(res, access_token)
    
    return {
        "data": {
            "id": created_user.id,
            "email": created_user.email,
            "username": created_user.username,
        }
    }

@auth_router.post("/login", response_model=Response, status_code=status.HTTP_200_OK)
async def login(res: HTTPResponse, user: LoginUser, user_service: user_service_dep):
    existing_user = await user_service.get_user_by_email(user.email)
    if not existing_user or not verify_password(
        user.password, existing_user.hashed_password
    ):
        raise AppException("Invalid email or password.", status_code=401)
    access_token = create_access_token(
        {
            "sub": {
                "id": existing_user.id,
                "email": existing_user.email,
                "username": existing_user.username,
                "role": existing_user.role,
            }
        },
    )
    set_cookies(res, access_token)
    return {
        "data": {
            "id": existing_user.id,
            "email": existing_user.email,
            "username": existing_user.username,
        }
    }


@auth_router.post("/logout", response_model=Response, status_code=status.HTTP_200_OK)
async def logout(req: Request, res: HTTPResponse, user_service: user_service_dep):
    token = req.cookies.get("access_jwt")
    if not token or not verify_access_token(token):
        raise AppException("Not authenticated.", status_code=401)
    id = verify_access_token(token).get("id")
    existing_user = await user_service.get_user_by_id(id)
    if not existing_user:
        raise AppException("User not found.", status_code=404)

    res.delete_cookie(key="access_jwt")
    return {"message": "Successfully logged out."}


@auth_router.get("/me", response_model=Response, status_code=status.HTTP_200_OK)
async def get_current_user(req: Request):
    token = req.cookies.get("access_jwt")
    if not token or not verify_access_token(token):
        raise AppException("Not authenticated.", status_code=401)
    sub = verify_access_token(token)
    return {"data": {**sub}}


@auth_router.get("/refresh", response_model=Response, status_code=status.HTTP_200_OK)
async def refresh_token(
    req: Request, res: HTTPResponse, user_service: user_service_dep
):
    token = req.cookies.get("access_jwt")
    if not token or not verify_access_token(token):
        raise AppException("Not authenticated.", status_code=401)
    id = verify_access_token(token).get("id")
    existing_user = await user_service.get_user_by_id(id)
    if not existing_user:
        raise AppException("User not found.", status_code=404)

    new_access_token = create_access_token(
        {
            "sub": {
                "id": existing_user.id,
                "email": existing_user.email,
                "username": existing_user.username,
                "role": existing_user.role,
            }
        }
    )
    set_cookies(res, new_access_token)
    return {
        "data": {
            "message": "Token refreshed successfully.",
        }
    }
