import json
from pathlib import Path
import httpx
from fastapi import HTTPException
from app.core.config import settings

ERROR_KEYWORD = [
    "error", "exception", "failed", "traceback",
    "critical", "warning", "timeout", "refused", "denied"
]

def read_log_file(filename:str) -> str:
    file_path = Path(settings.)