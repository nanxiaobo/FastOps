from fastapi import APIRouter
from app.schemas.ai_schema import LogAnalyzeRequest, LogAskRequest, LogExtractRequest
from app.services import ai_log_service

router = APIRouter(prefix="/ai", tags=["AI日志分析"])

@router.post("/log/analyze")
async def analyze_log(request: LogAnalyzeRequest):
    result = await ai_log_service.analyze_log(request.filename)
    return result

@router.post("/log/ask")
async def ask_log(request: LogAskRequest):
    result = await ai_log_service.ask_log(request.filename, request.question)
    return result

@router.post("/log/extract")
async def extract_log(request: LogExtractRequest):
    result = await ai_log_service.extract_log(request.filename)
    return result