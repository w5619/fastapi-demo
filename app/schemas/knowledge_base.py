from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING, Union

# 仅在类型检查时导入（不执行），解决Pylance误报
if TYPE_CHECKING:
    from app.schemas.document import DocumentRead
    from app.schemas.tag import TagRead

class KnowledgeBaseBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None

class KnowledgeBaseCreate(KnowledgeBaseBase):
    name: str
    tag_ids: Optional[List[Union[int| str]]] = []
    tag_names: List[str] = []  # 接收标签名称，如["abc", "def"]

class KnowledgeBaseUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None

    # 补充缺失的 add_tag_ids 字段
    add_tag_ids: Optional[List[int| str]] = []  # 用于添加标签的ID列表
    # 如果代码中还用到了 remove_tag_ids，也需要补充
    remove_tag_ids: Optional[List[int]] = None  # 用于移除标签的ID列表

class KnowledgeBaseRead(KnowledgeBaseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    # 字符串引用 + 类型注释，同时满足Pydantic和Pylance
    # documents: Optional[List['DocumentRead']] = None  # type: Optional[List[DocumentRead]]
    # tags: Optional[List['TagRead']] = None  # type: Optional[List[TagRead]]

    tags: List["TagRead"] = []  # 关联的标签
    
    class Config:
        from_attributes = True