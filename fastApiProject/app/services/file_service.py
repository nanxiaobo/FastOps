import os
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
    with open(save_path, 'w') as f:
        f.write(text)

