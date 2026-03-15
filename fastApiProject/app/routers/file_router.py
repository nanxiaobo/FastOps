import os.path

from fastapi import FastAPI, APIRouter, UploadFile, File
from app.services import file_service
from app.core.config import settings
from starlette.responses import FileResponse

router = APIRouter()


@router.post('/files/upload')
async def file_router(file: UploadFile = File(...)):
    result = await file_service.upload_file(file)
    return {'message': result,
            'file': file.filename,
            'size': file.size}


@router.get("/")
async def get_root():
    return FileResponse(os.path.join(settings.root_path, "index.html"))