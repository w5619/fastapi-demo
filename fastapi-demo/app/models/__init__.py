# 从当前目录导入所有模型类，方便外部统一导入

# 导入基础模型类
from app.models.base import BaseModel
# 导入知识库模型和关联表
from app.models.knowledge_base import KnowledgeBase, knowledge_base_tag
# 导入文档模型
from app.models.document import Document
# 导入标签模型
from app.models.tag import Tag

# 定义__all__，指定from app.models import *时要导入的内容
__all__ = [
    "BaseModel",
    "KnowledgeBase",
    "knowledge_base_tag",
    "Document",
    "Tag"
]