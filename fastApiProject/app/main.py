import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.scheduler import start_scheduler
from app.routers import router

app = FastAPI(title=settings.app_name,
              version=settings.app_version)

router.create_router(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

start_scheduler()

root_path_file = os.path.join(settings.html_path, "files.html")
@app.get("/files", response_class=HTMLResponse)
async def root():
    with open(root_path_file, "r", encoding="utf-8") as f:
        return f.read()

root_path_task = os.path.join(settings.html_path, "task.html")
@app.get("/tasks", response_class=HTMLResponse)
async def root():
    with open(root_path_task, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
