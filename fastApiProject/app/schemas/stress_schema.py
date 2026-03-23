from pydantic import BaseModel

class StressTestRequest(BaseModel):
    name: str
    method: str
    url: str
    concurrent: int  #并发数
    total: int
