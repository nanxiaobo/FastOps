import os
from pathlib import Path

from fastapi import HTTPException, File, UploadFile
from app.core.config import settings


async def upload_file(file: UploadFile):

    if not file.filename.endswith('.txt'):
        raise HTTPException(detail="仅支持txt文件上传", status_code=400)
    content = await file.read()
    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(detail="仅支持utf-8格式文件", status_code=400)
    save_path = os.path.join(settings.upload_dir, file.filename)
    with open(save_path, 'w', encoding="utf-8") as f:
        f.write(text)
    return "success"


async def get_file_list():
    file_list = []
    file_path = Path(settings.upload_dir)
    for file in file_path.iterdir():
        if file.is_file():
            file_list.append(
                {"filename": file.name, "size": file.stat().st_size}
            )
    return file_list

