import os
from pathlib import Path
from app.core.config import settings

async def get_log_content(filename: str):
    file_path = Path(settings.upload_dir)/filename
    if not file_path.exists():
        return {"error": "File not found"}
    with open(file_path, "r") as f:
        log_content = f.read()
    return {
        "filename": filename,
        "file_content": log_content}

async def search_log_content(filename: str, keyword: str):
    file_path = Path(settings.upload_dir) / filename
    if not file_path.exists():
        return {"error": "File not found"}
    result = []
    with open(file_path, "r",encoding="utf-8") as f:
        for line in f:
            if keyword.lower() in line.lower():
                result.append(line.strip())
    return {"filename": filename,
            "keyword": keyword,
            "file_count": len(result),
            "result": result[:50]}
