from fastapi import APIRouter, Header, HTTPException
from app.schemas.ai_schema import LogAnalyzeRequest, LogAskRequest, LogExtractRequest
from app.services import ai_log_service
from app.core.config import settings

router = APIRouter(prefix="/ai", tags=["AI日志分析"])


def verify_admin_token(x_admin_token: str):
    if not settings.task_admin_token:
        raise HTTPException(status_code=500, detail="服务端未配置 task_admin_token")

    if x_admin_token != settings.task_admin_token:
        raise HTTPException(status_code=403, detail="管理员 token 错误")


@router.post("/log/analyze")
async def analyze_log(
    request: LogAnalyzeRequest,
    x_admin_token: str = Header(default="")
):
    verify_admin_token(x_admin_token)
    result = await ai_log_service.analyze_log(request.filename)
    return result


@router.post("/log/ask")
async def ask_log(
    request: LogAskRequest,
    x_admin_token: str = Header(default="")
):
    verify_admin_token(x_admin_token)
    result = await ai_log_service.ask_log(request.filename, request.question)
    return result


@router.post("/log/extract")
async def extract_log(
    request: LogExtractRequest,
    x_admin_token: str = Header(default="")
):
    verify_admin_token(x_admin_token)
    result = await ai_log_service.extract_log(request.filename)
    return result

@router.get("/log/history")
async def get_log_history(x_admin_token: str = Header(default="")):
    verify_admin_token(x_admin_token)
    return ai_log_service.get_ai_log_history()

@router.get("/log/history/{history_id}")
async def get_log_history_detail(history_id: str, x_admin_token: str = Header(default="")):
    verify_admin_token(x_admin_token)
    return ai_log_service.get_ai_log_history_detail(history_id)