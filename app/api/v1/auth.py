from fastapi import APIRouter, Response as HTTPResponse, status, Request
from app.services import user_service_dep
from app.schemas import Response, UserCreate, LoginUser
from app.models import UserRole
from app.utils import create_access_token, verify_password, verify_access_token
from app.core import config, AppException, get_logger

logger = get_logger(__name__)

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
    logger.info(f"User signup request: email={user.email}, username={user.username}")
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
    logger.info(f"User registered successfully: id={created_user.id}")
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
    """Endpoint for admin registration."""
    logger.info(f"Admin signup request: email={user.email}, username={user.username}")
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
    logger.info(f"Admin registered successfully: id={created_user.id}")

    return {
        "data": {
            "id": created_user.id,
            "email": created_user.email,
            "username": created_user.username,
        }
    }

@auth_router.post("/login", response_model=Response, status_code=status.HTTP_200_OK)
async def login(res: HTTPResponse, user: LoginUser, user_service: user_service_dep):
    logger.info(f"Login attempt: email={user.email}")
    existing_user = await user_service.get_user_by_email(user.email)
    if not existing_user or not verify_password(
        user.password, existing_user.hashed_password
    ):
        logger.warning(f"Login failed: invalid credentials for email={user.email}")
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
    logger.info(f"User logged in successfully: id={existing_user.id}")
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
        logger.warning("Logout attempt: invalid or missing token")
        raise AppException("Not authenticated.", status_code=401)
    id = verify_access_token(token).get("id")
    existing_user = await user_service.get_user_by_id(id)
    if not existing_user:
        logger.warning(f"Logout attempt: user not found, id={id}")
        raise AppException("User not found.", status_code=404)

    res.delete_cookie(key="access_jwt")
    logger.info(f"User logged out: id={id}")
    return {"message": "Successfully logged out."}


@auth_router.get("/refresh", response_model=Response, status_code=status.HTTP_200_OK)
async def refresh_token(
    req: Request, res: HTTPResponse, user_service: user_service_dep
):
    token = req.cookies.get("access_jwt")
    if not token or not verify_access_token(token):
        logger.warning("Token refresh: invalid or missing token")
        raise AppException("Not authenticated.", status_code=401)
    id = verify_access_token(token).get("id")
    existing_user = await user_service.get_user_by_id(id)
    if not existing_user:
        logger.warning(f"Token refresh: user not found, id={id}")
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
    logger.info(f"Token refreshed for user: id={id}")
    return {
        "data": {
            "message": "Token refreshed successfully.",
        }
    }
