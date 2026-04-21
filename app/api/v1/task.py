from fastapi import APIRouter

task_router = APIRouter(prefix="/tasks", tags=["tasks"])

@task_router.get("/")