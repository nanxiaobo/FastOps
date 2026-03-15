import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import router

app = FastAPI(tittle=settings.app_name,
              version=settings.app_version)

router.create_router(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


root_path_file = os.path.join(settings.root_path, "files.html")


@app.get("/files", response_class=HTMLResponse)
async def root():
    with open(root_path_file, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
