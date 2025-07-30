from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

# 类型别名，简化依赖注入的类型注解
DbSession = Annotated[AsyncSession, Depends(get_db)]

# 可以在这里添加其他通用依赖项
# 例如：认证依赖、权限检查依赖等

async def example_dependency() -> str:
    """示例依赖项，返回当前环境"""
    from app.config import settings
    return settings.ENVIRONMENT
