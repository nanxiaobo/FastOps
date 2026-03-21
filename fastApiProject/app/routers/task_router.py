from fastapi import APIRouter
from app.schemas.task_scheam import TaskSchema
from app.services import task_service


router = APIRouter()

@router.get("/task")
async def get_tasks():
    result = await task_service.get_task()
    return result

@router.post("/task")
async def create_task(task: TaskSchema):
    result = await task_service.create_task(
        task_name=task.task_name,
        command=task.command,
        cron=task.cron
    )
    return result

@router.delete("/task/{task_id}")
async def delete_task(task_id: str):
    result = await task_service.delete_task(task_id)
    return result

@router.post("/task/{task_id}/run")
async def run_task_now(task_id: str):
    result = await task_service.run_task_now(task_id)
    return result

