from pydantic_settings import BaseSettings     # 从pydantic-settings导入BaseSettings基类
from pydantic import PostgresDsn     # 从pydantic导入PostgresDsn类型，用于验证PostgreSQL连接字符串
from typing import Optional     # 导入Optional类型，用于可选字段

from pydantic_settings import BaseSettings

class Settings(BaseSettings):     # 定义配置类，继承自BaseSettings
    DATABASE_URL: PostgresDsn     # 数据库配置 - 异步连接字符串
    DATABASE_URL_SYNC: PostgresDsn  # 数据库配置 - 同步连接字符串，用于Alembic

    # 补充 VERSION 字段
    VERSION: str = "0.1.0"  # 可根据实际版本号修改
    # 补充 API 前缀配置
    API_V1_STR: str = "/api/v1"  # 这是 FastAPI 常用的 API 版本前缀
    
    ENVIRONMENT: str = "development"  # 应用配置 - 环境标识，默认development
    API_PREFIX: str = "/api/v1"     # API路径前缀，默认/api/v1
    PROJECT_NAME: str = "FastApi Demo"    # 项目名称
    
    class Config:    # 配置读取来源
        env_file = ".env"  # 从.env文件读取配置
        case_sensitive = False  # 不区分大小写

settings = Settings()  # 创建配置实例，全局使用