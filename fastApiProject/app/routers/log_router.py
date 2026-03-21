from fastapi import APIRouter,Query
from app.services import log_service

router = APIRouter()


@router.get("/get_log_content")
async def get_log_content(filename: str):
    result = await log_service.get_log_content(filename)
    return {"文件内容为": result}


@router.get("/search_log")
async def search_log(filename: str = Query(...), keyword: str = Query(...)):
    result = await log_service.search_log_content(filename,keyword)
    return result


