import asyncio  #异步并发控制模块
import time
import uuid
import httpx

stress_list = []


async def stress_once(client: httpx.AsyncClient, method: str, url: str):
    # 单次请求
    start_time = time.time()
    try:
        if method.upper() == 'GET':
            response = await client.get(url)
        elif method.upper() == 'POST':
            response = await client.post(url)
        else:
            return {
                'success': False,
                'error': f'不支持的请求方法{method}',
                'status_code': None,
                'elapsed': 0
            }
        elapsed_time = time.time() - start_time
        success = 200 <= response.status_code < 400
        return {
            'success': success,
            'error': None,
            'status_code': response.status_code,
            'elapsed': elapsed_time
        }
    except Exception as e:
        elapsed_time = time.time() - start_time
        return {
            'success': False,
            'error': str(e),
            'status_code': None,
            'elapsed': elapsed_time
        }


# 执行函数
async def run_stress(method: str, url: str, concurrency: int, total: int):
    results = []
    semaphore = asyncio.Semaphore(concurrency)  # 限制并发数量

    async def bounded_task(client: httpx.AsyncClient):
        async with semaphore:
            return await stress_once(client, method, url)

    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [bounded_task(client) for _ in range(total)]
        results = await asyncio.gather(*tasks)
    return results

# 统计函数
def stress_summery(results: list):
    total = len(results)
    success_count = sum(1 for item in results if item['success'])
    fail_count = total - success_count
    elapsed_list = [item['elapsed'] for item in results]
    avg_time = sum(elapsed_list) / len(elapsed_list)
    max_time = max(elapsed_list) if elapsed_list else 0
    min_time = min(elapsed_list) if elapsed_list else 0
    success_rate = (success_count / total) * 100 if total else 0
    return {
        'total': total,
        'success_count': success_count,
        'fail_count': fail_count,
        'avg_time': avg_time,
        'max_time': max_time,
        'min_time': min_time,
    }

# 创建并执行
async def create_run_stress(name: str, method: str, url: str, concurrency: int, total: int):
    stress_id = str(uuid.uuid4())
    results = list(await run_stress(method=method, url=url, concurrency=concurrency, total=total))
    summery = stress_summery(results)
    stress_data = {
        'id': stress_id,
        'name': name,
        'method': method,
        'url': url,
        'concurrency': concurrency,
        'total': total,
        'summery': summery
    }
    stress_list.append(stress_data)
    return {"message": "压测已完成",
            "task": stress_data
    }

def get_stress_list():
    return {
        "message": "查询成功！",
        "total": len(stress_list),
        "stress_list": stress_list
    }