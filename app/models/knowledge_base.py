# 从SQLAlchemy导入列、字符串、文本类型
from sqlalchemy import Column, String, Text, Integer, Table, ForeignKey
# 从SQLAlchemy导入关系
from sqlalchemy.orm import relationship, DeclarativeBase
# 导入基础模型
from app.models.base import BaseModel

# 多对多关系表：知识库和标签的关联表
knowledge_base_tag = Table(
    "knowledge_base_tag",  # 表名
    BaseModel.metadata,  # 使用基本元数据
    # 关联表字段：
    # 知识库ID，外键关联到knowledgebases表的id字段
    Column("knowledge_base_id", Integer, ForeignKey("knowledgebases.id"), primary_key=True),
    # 标签ID，外键关联到tags表的id字段
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Base(DeclarativeBase):  # 关键：继承 AsyncAttrs 支持异步属性
    pass

# 知识库模型
class KnowledgeBase(BaseModel):
    """知识库模型"""
     # 表字段定义：
    # 主键ID，自增，索引
    id = Column(Integer, primary_key=True, index=True)
    # 名称，字符串类型，最大长度100，索引，非空
    name = Column(String(100), index=True, nullable=False)
    # 描述，文本类型，可为空
    description = Column(Text, nullable=True)
    

    # 关系定义：
    # 与文档的一对多关系：一个知识库可以有多个文档
    documents = relationship(
        "Document",  # 关联的模型
        back_populates="knowledge_base",  # 反向关联的属性名
        cascade="all, delete-orphan",  # 删除知识库时，同时删除关联的文档
        lazy="selectin"
    )
    
    # 与标签的多对多关系：一个知识库可以有多个标签，一个标签可以属于多个知识库
    tags = relationship(
        "Tag",  # 关联的模型
        secondary=knowledge_base_tag,  # 使用的关联表
        back_populates="knowledge_bases",  # 反向关联的属性名
        lazy="selectin"  # 支持预加载
    )