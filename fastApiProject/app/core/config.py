from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastOps"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///test.db"
    upload_dir: str = "app/uploads"


settings = Settings()
