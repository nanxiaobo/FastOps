import paramiko

def get_ssh_client(host: str, username: str, password: str, port: int, command:str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, username=username, password=password, timeout=5, port=port)

        stdin, stdout, stderr = client.exec_command(command)
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        return_code = stdout.channel.recv_exit_status()
        return {
            'return_code': return_code,
            'stdout': out,
            'stderr': err,
        }
    finally:
        client.close()