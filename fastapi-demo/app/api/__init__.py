# 导入 FastAPI 的路由管理工具 从fastapi导入APIRouter，用于集中管理路由
from fastapi import APIRouter

# 导入各个实体的路由模块
from app.api import knowledge_base, document, tag

# 创建API主路由实例，设置统一路由前缀
api_router = APIRouter(prefix="/api/v1")

# 将各个实体的路由包含到主路由中 
# prefix：为每个实体的路由添加子前缀（如 /knowledge-bases） 
# tags：用于 OpenAPI 文档分组，使 API 文档更清晰
api_router.include_router(knowledge_base.router, prefix="/knowledge-bases", tags=["knowledge-bases"])
api_router.include_router(document.router, prefix="/documents", tags=["documents"])
api_router.include_router(tag.router, prefix="/tags", tags=["tags"])