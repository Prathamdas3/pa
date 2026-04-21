from pwdlib import PasswordHash
from app.core import get_logger

logger = get_logger(__name__)

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    logger.debug("Hashing password")
    hashed = password_hash.hash(password)
    logger.debug("Password hashed successfully")
    return hashed


def verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.debug("Verifying password")
    result = password_hash.verify(plain_password, hashed_password)
    logger.debug(f"Password verification result: {result}")
    return result
