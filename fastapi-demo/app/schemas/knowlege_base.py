# 从pydantic导入基础模型和字段
from pydantic import BaseModel, Field
# 从datetime导入datetime类型
from datetime import datetime
# 从typing导入列表和可选类型
from typing import List, Optional
# 导入文档的读取模型
from app.schemas.document import DocumentRead
# 导入标签的读取模型
from app.schemas.tag import TagRead

# 基础模型，包含公共字段
class KnowledgeBaseBase(BaseModel):
    # 知识库名称，最大长度100，描述信息
    name: str = Field(..., max_length=100, description="知识库名称")
    # 知识库描述，可选
    description: Optional[str] = Field(None, description="知识库描述")

# 创建模型，用于创建新知识库
class KnowledgeBaseCreate(KnowledgeBaseBase):
    # 创建时可以指定标签ID列表，可选
    tag_ids: Optional[List[int]] = Field(None, description="关联的标签ID列表")

# 更新模型，用于更新知识库
class KnowledgeBaseUpdate(BaseModel):
    # 知识库名称，可选，最大长度100
    name: Optional[str] = Field(None, max_length=100, description="知识库名称")
    # 知识库描述，可选
    description: Optional[str] = Field(None, description="知识库描述")
    # 要添加的标签ID列表，可选
    add_tag_ids: Optional[List[int]] = Field(None, description="要添加的标签ID列表")
    # 要移除的标签ID列表，可选
    remove_tag_ids: Optional[List[int]] = Field(None, description="要移除的标签ID列表")

# 读取模型，用于返回知识库信息
class KnowledgeBaseRead(KnowledgeBaseBase):
    # 知识库ID
    id: int = Field(..., description="知识库ID")
    # 创建时间
    created_at: datetime = Field(..., description="创建时间")
    # 更新时间，可选
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    
    # 包含的文档列表，可选
    documents: Optional[List[DocumentRead]] = Field(None, description="包含的文档列表")
    # 关联的标签列表，可选
    tags: Optional[List[TagRead]] = Field(None, description="关联的标签列表")
    
    # 配置为允许ORM模型直接转换
    class Config:
        from_attributes = True