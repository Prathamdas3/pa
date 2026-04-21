from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
import sqlalchemy as sa
from app.core import get_logger

logger = get_logger(__name__)
logger.debug("Common models loaded")

class UserRole(Enum):
    user = "user"
    admin = "admin"

class TasksStatus(Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TasksPriority(Enum):
    low = "low"
    medium = "medium"
    high = "high"


class CreatedAtMixin(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={
            "nullable": False,
            "server_default": sa.func.now(),
            "index": True,
        }
    )

class UpdatedAtMixin(SQLModel):
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={
            "nullable": False,
            "server_default": sa.func.now(),
            "onupdate": sa.func.now(),
        }
    )