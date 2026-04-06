import json
from pathlib import Path
import httpx
from fastapi import HTTPException
from app.core.config import settings

ERROR_KEYWORD = [
    "error", "exception", "failed", "traceback",
    "critical", "warning", "timeout", "refused", "denied"
]

def read_log_file(filename: str) -> str:
    file_path = Path(settings.upload_dir) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_key_lines(log_text:str,context: int=2,max_lines:int=200) -> str:
    lines = log_text.split()
    selected_indexes = set()

    for i, line in enumerate(lines):
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in ERROR_KEYWORD):
            start = max(0,i-context)
            end = min(len(lines),i+context+1)
            for j in range(start,end):
                selected_indexes.add(j)
    selected_lines = [lines[i] for i in selected_indexes]
    if not selected_lines:
        selected_lines = lines[:max_lines]
    return "\n".join(selected_lines[:max_lines])

def build_analyze_prompt(log_text:str) -> str:
    return f"""
    你是一名资深运维故障分析助手。
    下面是一段系统日志，请你完成以下任务：
    1. 用简洁中文总结日志中最主要的问题
    2. 提取最关键的报错信息
    3. 判断问题严重级别（低/中/高）
    4. 给出可能原因
    5. 给出建议排查步骤
    6. 给出建议修复方案
    请严格按照以下 JSON 格式输出，不要输出其他内容：
    {{
    "summary":"",
    "severity": "",
    "errors": [],
    "possible_causes": [],
    "troubleshooting_steps": [],
    "solutions": []}}
    日志内容如下：
    {log_text}""".strip()

def build_ask_prompt(log_text: str, question: str) -> str:
    return f"""
    你是一名资深运维故障分析助手。
    下面给你一段日志内容，请基于日志回答用户问题。
    回答时要紧扣日志，不要凭空猜测；如果日志中没有足够信息，请明确说明。
    日志内容：
    {log_text}
    用户问题：
    {question}""".strip()

async def call_ai(prompt: str):
    api_key = settings.ai_api_key
    base_url = settings.ai_base_url
    model = settings.ai_model
    if not api_key:
        raise HTTPException(status_code=500, detail="未配置大模型 API Key")
    if not base_url:
        raise HTTPException(status_code=500, detail="未配置大模型 Base URL")
    if not model:
        raise HTTPException(status_code=500, detail="未配置大模型 Model")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个专业的运维AI助手"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"模型调用失败: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]


async def analyze_log(filename: str):
    raw_text = read_log_file(filename)
    key_text = extract_key_lines(raw_text)

    prompt = build_analyze_prompt(key_text)
    ai_result = await call_ai(prompt)

    try:
        parsed_result = json.loads(ai_result)
        return {
            "filename": filename,
            "analyze_result": parsed_result
        }
    except Exception:
        return {
            "filename": filename,
            "analyze_result": ai_result
        }


async def ask_log(filename: str, question: str):
    raw_text = read_log_file(filename)
    key_text = extract_key_lines(raw_text)

    prompt = build_ask_prompt(key_text, question)
    ai_result = await call_ai(prompt)

    return {
        "filename": filename,
        "question": question,
        "answer": ai_result
    }


async def extract_log(filename: str):
    raw_text = read_log_file(filename)
    key_text = extract_key_lines(raw_text)

    return {
        "filename": filename,
        "key_log_content": key_text
    }



