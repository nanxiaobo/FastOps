from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

engine = create_engine(settings.database_url)  #创建数据库引擎

SessionLocal = sessionmaker(  #创建session工厂，使用db = SessionLocal()建立连接
    autocommit=False,  #关闭自动提交事务,使用 db.commit() 提交
    autoflush=False,  #关闭自动同步，
    bind=engine)  #SessionLocal 绑定到 engine

Base = declarative_base()  #创建所有数据库表模型的父类 Base
