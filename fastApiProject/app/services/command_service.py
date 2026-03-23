import uuid
from app.utils.ssh_client import get_ssh_client

server_list = []

def add_server(name: str, host: str, port: int, username: str, password: str):
    server_id = str(uuid.uuid4())
    server_data = {
        'name': name,
        'host': host,
        'port': port,
        'username': username,
        'password': password,
        'server_id': server_id
    }
    server_list.append(server_data)
    return {"message": "Server added successfully",
            "server": {
                'id': server_id,
                'name': name,
                'host': host,
                'port': port,
                'username': username,
    }}

def get_server():
    safe_server_list = []
    for server in server_list:
        safe_server_list.append(
            {
                'id': server['server_id'],
                'name': server['name'],
                'host': server['host'],
                'port': server['port'],
                'username': server['username'],
            }
        )
    return {"message": "Get server list success!",
            "servers": safe_server_list,
            'total': len(server_list)}


def run_command(command: str, server_id: str):
    for server in server_list:
        if server['server_id'] == server_id:
            result = get_ssh_client(
                host=server['host'],
                port=server['port'],
                username=server['username'],
                password=server['password'],
                command=command
            )
            return {"message": "Command executed successfully!",
                    "command": command,
                    "server_id": server_id,
                    "result": result}
    return {"message": "Client not found!"}


def delete_server(server_id: str):
    for server in server_list:
        if server["server_id"] == server_id:
            server_list.remove(server)
            return {
                "message": "Server deleted successfully!",
                "deleted_server": {
                    "id": server["server_id"],
                    "name": server["name"],
                    "host": server["host"],
                    "port": server["port"],
                    "username": server["username"]
                }
            }
    return {"message": "Server not found!"}

