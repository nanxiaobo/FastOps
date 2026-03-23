from fastapi import FastAPI
from app.routers import file_router, log_router, translate, task_router, command_router,stress_router
from app.routers.translate import router


def create_router(app: FastAPI):
    app.include_router(file_router.router)
    app.include_router(log_router.router)
    app.include_router(translate.router)
    app.include_router(task_router.router)
    app.include_router(command_router.router)
    app.include_router(stress_router.router)