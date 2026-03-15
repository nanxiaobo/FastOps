from fastapi import FastAPI, APIRouter, UploadFile, File
from starlette.responses import FileResponse

router = APIRouter()


@router.post('/files/upload')
async def file_router(file: UploadFile = File(...)):
    return {'message': "success",
            'file': file.filename,
            'size': file.size}


@router.get("/")
async def get_root():
    return FileResponse("frontend/index.html")