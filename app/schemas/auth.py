from app.core import CustomBaseModel
from pydantic import Field, EmailStr, field_validator
import re

WEAK_PASSWORDS = ["password", "12345678", "password123", "qwerty123", "admin123"]


def validate_password_rules(v: str) -> str:
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
        raise ValueError("Password must contain at least one special character")
    if re.search(r"\s", v):
        raise ValueError("Password must not contain spaces")
    if v.lower() in WEAK_PASSWORDS:
        raise ValueError("Password is too common, choose a stronger one")
    return v


class UserBase(CustomBaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        banned_usernames = ["admin", "root", "superuser"]
        if v.lower() in banned_usernames:
            raise ValueError("This username is reserved")
        return v


class UserCreate(UserBase):
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_rules(v)


class LoginUser(CustomBaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_rules(v)