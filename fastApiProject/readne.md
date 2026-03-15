**综合运维工具平台**

项目简介：基于 FastAPI 独立开发的综合运维平台，集成远程命令执行、日志分析、任务调度、文件管理与 API 压测功能，支持任务记录持久化、日志解析、异步并发请求及文件流式处理，后续待植入ai分析等



# 项目结构

```
FastOps/
├── app/                       ---业务代码
│   ├── main.py                ---创建 FastAPI 应用，注册路由，启动配置
│   ├── core/   
│   │   ├── config.py          ---全局配置
│   │   ├── database.py        ---数据库连接初始化
│   │   └── security.py        ---登录认证 / JWT(token生成，token验证，密码加密)
│   ├── models/                ---数据库表结构
│   │   ├── task.py
│   │   ├── file_record.py
│   │   ├── command.py
│   │   ├── log_record.py
│   │   └── stress_test.py
│   ├── schemas/               ---请求 / 返回的数据模型(使用 Pydantic，API请求参数校验，API返回格式规范)
│   │   ├── task_schema.py
│   │   ├── file_schema.py
│   │   ├── command_schema.py
│   │   ├── log_schema.py
│   │   └── stress_schema.py
│   ├── routers/               ---接口路由
│   │   ├── command_router.py
│   │   ├── log_router.py
│   │   ├── task_router.py
│   │   ├── file_router.py
│   │   └── stress_router.py
│   ├── services/              ---业务逻辑
│   │   ├── command_service.py
│   │   ├── log_service.py
│   │   ├── task_service.py
│   │   ├── file_service.py
│   │   └── stress_service.py
│   ├── utils/                 ---工具函数
│   │   ├── ssh_client.py      ---远程执行命令
│   │   ├── log_parser.py      ---日志解析工具
│   │   └── response.py        ---统一返回格式
│   └── uploads/               ---上传的文件
├── requirements.txt
└── README.md
```

一个完整的请求流程如下：

```
用户请求
↓
router
↓
schema校验
↓
service处理逻辑
↓
utils工具
↓
model写数据库
↓
返回response
```

执行项目之前请先在终端执行以下代码

```
python.exe -m pip install --upgrade pip
pip install -r .\requirements.txt
```


