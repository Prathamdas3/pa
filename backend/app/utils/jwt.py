from datetime import UTC, datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from app.core import config, get_logger

logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scheme_name="JWT")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    logger.debug("Creating JWT access token")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=config.access_token_expire_minutes,
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        config.secret_key,
        algorithm=config.algorithm,
    )
    logger.debug("JWT access token created successfully")
    return encoded_jwt


def verify_access_token(token: str):
    try:
        decoded = jwt.decode(
            token,
            options={"verify_signature": False, "verify_exp": True},
            algorithms=[config.algorithm],
        )
        exp = decoded.get("exp")
        if exp and datetime.now(UTC).timestamp() > exp:
            logger.warning("JWT token expired")
            return None
        sub = decoded.get("sub")
        if sub is None:
            return None
        if isinstance(sub, dict):
            return sub
        return {"id": sub}
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"JWT token verification failed: {e}")
        return None