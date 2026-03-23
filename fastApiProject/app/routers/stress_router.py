from fastapi import APIRouter
from app.schemas.stress_schema import  StressTestRequest
from app.services import stress_service

router = APIRouter()

@router.post("/stress_run")
async def run_stress_test(data: StressTestRequest):
    return await stress_service.create_run_stress(
        name=data.name,
        method=data.method,
        url=data.url,
        concurrency=data.concurrent,
        total=data.total
    )


@router.get("/stress_history")
def get_stress_list():
    return stress_service.get_stress_list()
