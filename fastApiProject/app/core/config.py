import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).resolve().parents[2]   # fastApiProject
APP_DIR = PROJECT_DIR / "app"
html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
class Settings(BaseSettings):
    app_name: str = "FastOps"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///test.db"
    upload_dir: str = upload_dir
    html_path: str = html_path
    task_admin_token: str = ""   #任务调度的管理员口令
    ai_api_key: str = ""
    ai_base_url: str = ""
    ai_model: str = ""
    model_config = SettingsConfigDict(
        env_file=(
            str(PROJECT_DIR / ".env"),
            str(PROJECT_DIR / ".env.prod")),
        env_file_encoding="utf-8",
        extra="ignore")


settings = Settings()


