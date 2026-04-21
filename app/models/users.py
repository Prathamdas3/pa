
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
import sqlalchemy as sa
from .common import CreatedAtMixin, UpdatedAtMixin, UserRole
from app.core import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from .tasks import Tasks


class Users(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    """User account model.

    Attributes:
        username: Unique display name.
        email: Unique email address.
        hashed_password: Bcrypt hashed password.
        role: User role, either user or admin.
        is_active: Soft delete / account status flag.
        taskss: Related tasks items.
    """

    username: str = Field(
        sa_column=sa.Column(sa.String(), nullable=False, index=True, unique=True)
    )
    email: EmailStr = Field(
        sa_column=sa.Column(sa.String(), nullable=False, index=True, unique=True)
    )
    hashed_password: str = Field(nullable=False)

    role: UserRole = Field(
        sa_column=sa.Column(
            sa.Enum(UserRole),
            nullable=False,
            server_default=UserRole.user.value,
        )
    )

    is_active: bool = Field(
        sa_column=sa.Column(sa.Boolean(), nullable=False, server_default=sa.true())
    )

    Taskss: list["Tasks"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )