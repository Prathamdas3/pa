from app.services.users import UserService
from app.services.tasks import TaskService
from app.repository import TaskRepo,UserRepo
from app.core import SessionDep
from typing import Annotated
from fastapi import Depends

async def init_user_service(session:SessionDep):
    repo=UserRepo(session=session)
    return UserService(repo)

async def init_task_service(session:SessionDep):
    repo=TaskRepo(session=session)
    return TaskService(repo)

user_service_dep = Annotated[UserService, Depends(init_user_service)]
task_service_dep = Annotated[TaskService, Depends(init_task_service)]

__all__ = [
    "UserService",
    "TaskService",
    "user_service_dep",
    "task_service_dep",
]