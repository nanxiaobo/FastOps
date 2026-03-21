import os

from pydantic_settings import BaseSettings

html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
class Settings(BaseSettings):
    app_name: str = "FastOps"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///test.db"
    upload_dir: str = upload_dir
    html_path: str = html_path


settings = Settings()
