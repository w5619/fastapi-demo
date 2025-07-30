# 从SQLAlchemy导入列、字符串、整数类型
from sqlalchemy import Column, String, Integer
# 从SQLAlchemy导入关系
from sqlalchemy.orm import relationship
# 导入基础模型
from app.models.base import BaseModel
# 导入多对多关系的关联表
from app.models.knowledge_base import knowledge_base_tag

# 标签模型
class Tag(BaseModel):
    """标签模型"""
    # 主键ID，自增，索引
    id = Column(Integer, primary_key=True, index=True)
    # 名称，字符串类型，最大长度50，唯一，索引，非空
    name = Column(String(50), unique=True, index=True, nullable=False)
    # 标签颜色，字符串类型，可为空，默认灰色
    color = Column(String(20), nullable=True, default="#cccccc")
    
    # 与知识库的多对多反向关系
    knowledge_bases = relationship(
        "KnowledgeBase",  # 关联的模型
        secondary=knowledge_base_tag,  # 使用的关联表
        back_populates="tags",  # 反向关联的属性名
        lazy="selectin"  # 关键：使用 selectin 支持异步预加载
    )