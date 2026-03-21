import os

from fastapi import Form, APIRouter
from fastapi.responses import HTMLResponse
from app.core.config import settings
from googletrans import Translator

router = APIRouter()

translator = Translator()


@router.get("/files", response_class=HTMLResponse)
async def index():
    file_path = os.path.join(settings.html_path, "files.html")
    if not os.path.exists(file_path):
        return HTMLResponse(content=f"找不到文件: {file_path}", status_code=404)

    with open(file_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@router.post("/translate")
async def translate(
    text: str = Form(...),
    target_lang: str = Form(...)
):
    result = await translator.translate(text, dest=target_lang)

    return {
        "original_text": text,
        "translated_text": result.text,
        "target_lang": target_lang
    }