from pydantic import BaseModel


class TaskSchema(BaseModel):
    task_name: str
    command: str
    cron: str
    