import uuid  #用于生成唯一id
import subprocess  #用于执行shell命令
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger  #CronTrigger 用来根据 cron 表达式创建定时触发器
from app.core.scheduler import scheduler

task_store = []  #临时使用，保存任务信息

async def run_command(task_id: str, command: str):
    result = subprocess.run(command,    #使用subprocess.run执行命令
                            shell=True,     #由系统shell执行
                            stdout=subprocess.PIPE,    #获取输出和报错
                            stderr=subprocess.PIPE,    #按字符串处理输出结果
                            text=True,     #直接返回字符串，不加这个的话运行报错
                            encoding="utf-8",   #统一格式，windows可能乱码，但不会崩掉
                            errors="ignore"
                            )
    return {
        'task_id': task_id,
        "command": command,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "return code": result.returncode
    }

async def create_task(task_name:str, command:str, cron:str):
    task_id = str(uuid.uuid4())
    if cron == "now":   #立即执行
        scheduler.add_job(
            func=run_command,
            args=[task_id, command],
            trigger="date",
            run_date=datetime.now(),
            id=task_id,
            name=task_name,
            replace_existing=True
        )
        task_data = {
            "task_id": task_id,
            "task_name": task_name,
            "command": command,
            "cron": cron
        }
        task_store.append(task_data)
        return {"message": "Create task success!", "data": task_data}

    cron_parts = cron.split()  #定时任务
    if len(cron_parts) != 5:
        return {"error":"cron表达式应该有5段！"}
    trigger = CronTrigger(
        minute=cron_parts[0],
        hour=cron_parts[1],
        day=cron_parts[2],
        month=cron_parts[3],
        day_of_week=cron_parts[4]
    )
    scheduler.add_job(
        func=run_command,
        args=[task_id, command],
        trigger=trigger,
        id=task_id,
        name=task_name,
        replace_existing=True
    )
    task_data = {"task_id": task_id, "task_name": task_name, "command": command, "cron": cron}
    task_store.append(task_data)
    return {"message":"Create task success!", "data":task_data}

async def get_task():
    return {"message":"Get task success!", "total":len(task_store), "data": task_store}

async def run_task_now(task_id: str):
    for task in task_store:
        if task["task_id"] == task_id:
            return await run_command(task_id, task["command"])
    return {"message":"Task not found!"}

async def delete_task(task_id: str):
    try:
        scheduler.remove_job(task_id)
    except Exception:
        pass

    for index, task in enumerate(task_store):
        if task["task_id"] == task_id:
            deletetask = task_store.pop(index)
            return {"message":"Delete task success!", "data":deletetask}
        return {"error":"Task not found!"}
