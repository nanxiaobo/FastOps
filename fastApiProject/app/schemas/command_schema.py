from pydantic import BaseModel

class ServerCreate(BaseModel):
    name : str
    host : str
    port : int = 22
    username : str
    password : str

class CommandExecute(BaseModel):
    server_id: str
    command: str
