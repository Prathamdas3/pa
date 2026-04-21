from app.core import CustomBaseModel
from pydantic import Field, field_validator, model_validator
from app.models import TasksPriority,TasksStatus
from datetime import datetime, timezone


class TaskCreate(CustomBaseModel):
    """Schema for creating a new task."""

    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        examples=["Buy groceries"],
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
    )
    priority: TasksPriority = Field(default=TasksPriority.medium)
    status: TasksStatus = Field(default=TasksStatus.pending)
    due_date: datetime | None = Field(default=None)
    tags: list[str] | None = Field(default=None)

    # ── Field Validators ──────────────────────────────────────────────────────

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be blank or whitespace only.")
        return v.strip()

    @field_validator("description")
    @classmethod
    def clean_description(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Description cannot be blank whitespace.")
        return v.strip() if v else None

    @field_validator("due_date")
    @classmethod
    def due_date_must_be_future(cls, v: datetime | None) -> datetime | None:
        if v is not None and v < datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future.")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        if len(v) > 10:
            raise ValueError("A task cannot have more than 10 tags.")
        cleaned = [tag.strip().lower() for tag in v]
        if any(len(tag) == 0 for tag in cleaned):
            raise ValueError("Tags cannot be empty strings.")
        if any(len(tag) > 30 for tag in cleaned):
            raise ValueError("Each tag must be 30 characters or less.")
        if len(cleaned) != len(set(cleaned)):
            raise ValueError("Duplicate tags are not allowed.")
        return cleaned

    # ── Model Validator ───────────────────────────────────────────────────────

    @model_validator(mode="after")
    def completed_task_must_not_have_future_due_date(self) -> "TaskCreate":
        if self.status == TasksStatus.completed and self.due_date is not None:
            if self.due_date > datetime.now(timezone.utc):
                raise ValueError("A completed task cannot have a future due date.")
        return self
    
    
class TaskUpdate(CustomBaseModel):
    """Schema for updating a task — all fields optional."""

    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
    )
    priority: TasksPriority | None = Field(default=None)
    status: TasksStatus | None = Field(default=None)
    due_date: datetime | None = Field(default=None)
    tags: list[str] | None = Field(default=None)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be blank or whitespace only.")
        return v.strip() if v else None

    @field_validator("due_date")
    @classmethod
    def due_date_must_be_future(cls, v: datetime | None) -> datetime | None:
        if v is not None and v < datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future.")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        if len(v) > 10:
            raise ValueError("A task cannot have more than 10 tags.")
        cleaned = [tag.strip().lower() for tag in v]
        if any(len(tag) == 0 for tag in cleaned):
            raise ValueError("Tags cannot be empty strings.")
        if any(len(tag) > 30 for tag in cleaned):
            raise ValueError("Each tag must be 30 characters or less.")
        if len(cleaned) != len(set(cleaned)):
            raise ValueError("Duplicate tags are not allowed.")
        return cleaned

    @model_validator(mode="after")
    def at_least_one_field(self) -> "TaskUpdate":
        """Prevent empty PATCH requests."""
        if not any(
            v is not None
            for v in [self.title, self.description, self.priority, self.status, self.due_date, self.tags]
        ):
            raise ValueError("At least one field must be provided to update.")
        return self