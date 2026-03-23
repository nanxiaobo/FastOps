import secrets

from fastapi import APIRouter, Header, HTTPException

from app.core.config import settings
from app.schemas.task_scheam import TaskSchema
from app.services import task_service


router = APIRouter()

def verify_task_token(x_admin_token: str = Header(default="")):
    """
    校验请求头里的 X-Admin-Token
    """
    if not settings.task_admin_token:
        raise HTTPException(status_code=500, detail="服务端未配置 TASK_ADMIN_TOKEN")

    if not secrets.compare_digest(x_admin_token, settings.task_admin_token):
        raise HTTPException(status_code=401, detail="没有权限执行该操作")

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

