# 从当前目录导入所有Pydantic模型，方便外部统一导入   
# 批量导入所有 Pydantic 模型类，按实体类型分组
from app.schemas.knowledge_base import (
    KnowledgeBaseBase,
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    KnowledgeBaseRead
)
from app.schemas.document import (
    DocumentBase,
    DocumentCreate,
    DocumentUpdate,
    DocumentRead
)
from app.schemas.tag import (
    TagBase,
    TagCreate,
    TagUpdate,
    TagRead
)

# 定义__all__，指定通配符导入时包含的内容
__all__ = [
    # 知识库相关模型
    "KnowledgeBaseBase",
    "KnowledgeBaseCreate",
    "KnowledgeBaseUpdate",
    "KnowledgeBaseRead",
    # 文档相关模型
    "DocumentBase",
    "DocumentCreate",
    "DocumentUpdate",
    "DocumentRead",
    # 标签相关模型
    "TagBase",
    "TagCreate",
    "TagUpdate",
    "TagRead"
]