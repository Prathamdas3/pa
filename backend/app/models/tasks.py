from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlmodel import Field, Relationship
import sqlalchemy as sa
from .common import CreatedAtMixin, UpdatedAtMixin, TasksStatus, TasksPriority
from app.core import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from .users import Users


class Tasks(CreatedAtMixin, UpdatedAtMixin, table=True):
    """Tasks item model.

    Attributes:
        title: Short title of the tasks.
        description: Optional detailed description.
        status: Current status of the tasks.
        priority: Priority level of the tasks.
        due_date: Optional deadline for the tasks.
        is_deleted: Soft delete flag.
        user_id: Foreign key reference to the owner.
        user: Related user object.
    """

    title: str = Field(sa_column=sa.Column(sa.String(), nullable=False, index=True))
    description: Optional[str] = Field(sa_column=sa.Column(sa.Text(), nullable=True))

    status: TasksStatus = Field(
        sa_column=sa.Column(
            sa.Enum(TasksStatus),
            nullable=False,
            server_default=TasksStatus.pending.value,
        )
    )

    priority: TasksPriority = Field(
        sa_column=sa.Column(
            sa.Enum(TasksPriority),
            nullable=False,
            server_default=TasksPriority.medium.value,
        )
    )

    due_date: Optional[str] = Field(default=None, nullable=True)

    is_deleted: bool = Field(
        sa_column=sa.Column(sa.Boolean(), nullable=False, server_default=sa.false())
    )

    tags: list[str] | None = Field(
        default=None, sa_column=sa.Column(sa.JSON(), nullable=True)
    )

    user_id: UUID = Field(
        sa_column=sa.Column(
            sa.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )

    user: "Users" = Relationship(back_populates="Tasks")
