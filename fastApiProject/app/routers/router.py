from fastapi import FastAPI
from app.routers import file_router


def create_router(app: FastAPI):
    app.include_router(file_router.router)