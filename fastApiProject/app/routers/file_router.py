import os.path

from fastapi import FastAPI, APIRouter, UploadFile, File
from app.services import file_service
from app.core.config import settings
from starlette.responses import FileResponse

router = APIRouter()

@router.get("/")
async def get_root():
    return FileResponse(os.path.join(settings.root_path, "index.html"))

@router.post('/files/upload')
async def file_router(file: UploadFile = File(...)):
    result = await file_service.upload_file(file)
    return {'message': result,
            'filename': file.filename,
            'size': file.size}

@router.get('/files/list')
async def get_files():
    result = await file_service.get_file_list()
    return {'files': result}



