from uuid import UUID
from fastapi import APIRouter, status, Request, Depends
from app.core import AppException, get_logger
from app.utils import verify_access_token
from app.schemas import TaskCreate, Response, TaskUpdate
from app.services import task_service_dep
from app.dependencies import get_current_user, require_admin, CurrentUser

logger = get_logger(__name__)

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_current_user_id(req: Request) -> UUID:
    """Dependency to extract and verify JWT from cookies, returning the user ID."""
    token = req.cookies.get("access_jwt")
    if not token:
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, message="Unauthorized")
    payload = verify_access_token(token)
    if not payload:
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, message="Unauthorized")
    id=payload.get("id")
    try:
        return UUID(id)
    except ValueError:
        raise AppException(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid user ID format")


@task_router.get("/", response_model=Response, status_code=status.HTTP_200_OK)
async def get_tasks(task_service: task_service_dep, user_id: UUID = Depends(get_current_user_id)):
    """Endpoint to retrieve all tasks for the authenticated user."""
    logger.debug(f"Get all tasks: user_id={user_id}")
    tasks = await task_service.get_tasks_by_user_id(user_id)
    logger.info(f"Retrieved {len(tasks)} tasks for user_id={user_id}")
    return {"data": tasks}


@task_router.get("/{task_id}", response_model=Response, status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: UUID, task_service: task_service_dep, user_id: UUID = Depends(get_current_user_id)):
    """Endpoint to retrieve a specific task by ID for the authenticated user."""
    logger.debug(f"Get task: task_id={task_id}, user_id={user_id}")
    task = await task_service.get_task_by_id(task_id, user_id=user_id)
    return {"data": task}


@task_router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create_task(task_create: TaskCreate, task_service: task_service_dep, user_id: UUID = Depends(get_current_user_id)):
    """Endpoint to create a new task for the authenticated user."""
    logger.info(f"Create task: title={task_create.title}, user_id={user_id}")
    task = await task_service.create_task(task_create, user_id=user_id)
    logger.info(f"Task created: task_id={task.id}")
    return {"data": task}


@task_router.delete("/{task_id}", response_model=Response, status_code=status.HTTP_200_OK)
async def delete_task(task_id: UUID, task_service: task_service_dep, user_id: UUID = Depends(get_current_user_id)):
    """Endpoint to delete a task by ID for the authenticated user."""
    logger.info(f"Delete task: task_id={task_id}, user_id={user_id}")
    await task_service.delete_task(task_id, user_id=user_id)
    logger.info(f"Task deleted: task_id={task_id}")
    return {"data": {"message": "Task deleted successfully."}}


@task_router.patch("/{task_id}", response_model=Response, status_code=status.HTTP_200_OK)
async def update_task(task_id: UUID, task_update: TaskUpdate, task_service: task_service_dep, user_id: UUID = Depends(get_current_user_id)):
    """Endpoint to update a task by ID for the authenticated user."""
    logger.info(f"Update task: task_id={task_id}, user_id={user_id}")
    task = await task_service.update_task(task_id, task_update, user_id=user_id)
    logger.info(f"Task updated: task_id={task_id}")
    return {"data": task}


@task_router.get("/admin/all", response_model=Response, status_code=status.HTTP_200_OK)
async def admin_get_all_tasks(task_service: task_service_dep, _: CurrentUser = Depends(require_admin)):
    """Admin: get ALL tasks across all users."""
    logger.info("Admin: fetching all tasks")
    tasks = await task_service.get_all_tasks()
    logger.info(f"Admin: retrieved {len(tasks)} tasks")
    return {"data": tasks}


@task_router.get("/admin/{task_id}", response_model=Response, status_code=status.HTTP_200_OK)
async def admin_get_task_by_id(task_id: UUID, task_service: task_service_dep, _: CurrentUser = Depends(require_admin)):
    """Admin: get any task by ID."""
    logger.info(f"Admin: fetching task_id={task_id}")
    task = await task_service.get_task_by_id_admin(task_id)
    return {"data": task}


@task_router.delete("/admin/{task_id}", response_model=Response, status_code=status.HTTP_200_OK)
async def admin_delete_task(task_id: UUID, task_service: task_service_dep, _: CurrentUser = Depends(require_admin)):
    """Admin: delete any task regardless of owner."""
    logger.info(f"Admin: deleting task_id={task_id}")
    await task_service.delete_task_admin(task_id)
    return {"data": {"message": "Task deleted by admin."}}