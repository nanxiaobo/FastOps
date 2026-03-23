from fastapi import APIRouter
from app.schemas.command_schema import ServerCreate, CommandExecute
from app.services import command_service

router = APIRouter()

@router.get("/command")
async def get_server_list():
    return command_service.get_server()

@router.post("/command")
async def create_server(data: ServerCreate):
    return command_service.add_server(
        name=data.name,
        port=data.port,
        host=data.host,
        username=data.username,
        password=data.password
    )

@router.post("/command/run")
async def run_command(data: CommandExecute):
    return command_service.run_command(
        command=data.command,
        server_id=data.server_id
    )

@router.delete("/command/{server_id}")
async def delete_server(server_id):
    return command_service.delete_server(server_id=server_id)