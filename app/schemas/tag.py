from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.knowledge_base import KnowledgeBaseRead

class TagBase(BaseModel):
    name: str = Field(..., max_length=50)
    color: Optional[str] = Field("#cccccc", pattern=r'^#([A-Fa-f0-9]{6})$')

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, pattern=r'^#([A-Fa-f0-9]{6})$')

class TagRead(TagBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    # 字符串引用 + 类型注释
    knowledge_bases: Optional[List['KnowledgeBaseRead']] = None  # type: Optional[List[KnowledgeBaseRead]]
    
    class Config:
        from_attributes = True