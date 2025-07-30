# 从SQLAlchemy导入列、字符串、文本、外键、整数类型
from sqlalchemy import Column, String, Text, ForeignKey, Integer
# 从SQLAlchemy导入关系
from sqlalchemy.orm import relationship
# 导入基础模型
from app.models.base import BaseModel

# 文档模型
class Document(BaseModel):
    """文档模型"""
    # 字段定义：
    # 主键ID，自增，索引
    id = Column(Integer, primary_key=True, index=True)
    # 标题，字符串类型，最大长度200，索引，非空
    title = Column(String(200), index=True, nullable=False)
    # 内容，文本类型，非空
    content = Column(Text, nullable=False)
    
    # 外键：关联到知识库
    knowledge_base_id = Column(
        Integer, 
        # 外键关联到knowledgebases表的id字段，当知识库删除时，文档也删除
        ForeignKey("knowledgebases.id", ondelete="CASCADE"),
        nullable=False  # 不允许为空，确保每个文档都属于一个知识库
    )
    
    # 关系定义: 文档 -> 知识库   与知识库的反向关系
    knowledge_base = relationship(
        "KnowledgeBase",  # 关联的模型
        back_populates="documents"  # 反向关联的属性名
    )