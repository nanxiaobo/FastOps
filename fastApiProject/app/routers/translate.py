from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from googletrans import Translator

router = APIRouter()

templates = Jinja2Templates(directory="frontend")
translator = Translator()


@router.get("/files", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("files.html", {"request": request})


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