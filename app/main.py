from fastapi import FastAPI
from app.api import api_router  # 确保导入了你的路由
from app.config import settings

# 实例化 FastAPI 时，默认已启用 docs 和 redoc
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API 文档描述",
    # 以下参数默认开启，若之前手动关闭了需移除
    # docs_url=None,  # 不要设置这个，否则会禁用 Swagger UI
    # redoc_url=None  # 不要设置这个，否则会禁用 ReDoc
)

# 挂载路由（关键：必须挂载路由，否则文档可能为空或无法访问）
app.include_router(api_router, prefix=settings.API_V1_STR)

# 可选：添加根路径路由（方便测试）
@app.get("/")
def read_root():
    return {"message": "Welcome to the API. Visit /docs for documentation."}