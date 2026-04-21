"""Common models and mixins.

Contains shared enums and SQLModel mixins for timestamp fields.
"""

from uuid import UUID, uuid4
from enum import Enum
from sqlalchemy.orm import declared_attr
from sqlmodel import Field
import sqlalchemy as sa
from app.core import get_logger

logger = get_logger(__name__)

logger.debug("Common models loaded")


class UserRole(Enum):
    """User role enumeration.

    Attributes:
        user: Regular user with access to own Tasks only.
        admin: Admin user with access to all Tasks.
    """
    user = "user"
    admin = "admin"


class TasksStatus(Enum):
    """Task item status enumeration.

    Attributes:
        pending: Task has not been started.
        in_progress: Task is currently being worked on.
        completed: Task has been finished.
    """
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TasksPriority(Enum):
    """Task item priority enumeration.

    Attributes:
        low: Low priority task.
        medium: Medium priority task.
        high: High priority task.
    """
    low = "low"
    medium = "medium"
    high = "high"


# ---------------- MIXINS ----------------

class CreatedAtMixin:
    """Mixin for UUID primary key and created_at timestamp."""

    __allow_unmapped__ = True

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    @declared_attr
    def created_at(cls):
        return sa.Column(
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            index=True,
        )


class UpdatedAtMixin:
    """Mixin for updated_at auto-updating timestamp."""

    __allow_unmapped__ = True

    @declared_attr
    def updated_at(cls):
        return sa.Column(
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        )