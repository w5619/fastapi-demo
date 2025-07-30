# 从当前目录导入所有CRUD函数，方便外部统一导入   
# 导入所有 CRUD 操作函数，按实体类型组织  
# 这样其他模块（如 API 路由）可以直接从 app.crud 导入所需的操作函数
from app.crud.knowledge_base import (
    create_knowledge_base,
    get_knowledge_base,
    get_knowledge_bases,
    update_knowledge_base,
    delete_knowledge_base
)
from app.crud.document import (
    create_document,
    get_document,
    get_documents,
    update_document,
    delete_document
)
from app.crud.tag import (
    create_tag,
    get_tag,
    get_tags,
    update_tag,
    delete_tag
)

# 定义__all__，指定通配符导入时包含的内容
__all__ = [
    # 知识库相关CRUD
    "create_knowledge_base",
    "get_knowledge_base",
    "get_knowledge_bases",
    "update_knowledge_base",
    "delete_knowledge_base",
    # 文档相关CRUD
    "create_document",
    "get_document",
    "get_documents",
    "update_document",
    "delete_document",
    # 标签相关CRUD
    "create_tag",
    "get_tag",
    "get_tags",
    "update_tag",
    "delete_tag"
]