# 从当前目录导入所有Pydantic模型，方便外部统一导入   
# 批量导入所有 Pydantic 模型类，按实体类型分组
# 导入所有模型
from app.schemas.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseRead, KnowledgeBaseUpdate
from app.schemas.document import DocumentCreate, DocumentRead, DocumentUpdate
from app.schemas.tag import TagCreate, TagRead, TagUpdate

# 关键：所有模型定义完成后，统一重建类型引用
KnowledgeBaseRead.model_rebuild()
DocumentRead.model_rebuild()
TagRead.model_rebuild()

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