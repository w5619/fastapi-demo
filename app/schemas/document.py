from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.knowledge_base import KnowledgeBaseRead

class DocumentBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str

class DocumentCreate(DocumentBase):
    knowledge_base_id: int

class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None

class DocumentRead(DocumentBase):
    id: int
    knowledge_base_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    # 字符串引用 + 类型注释
    # knowledge_base: Optional['KnowledgeBaseRead'] = None  # type: Optional[KnowledgeBaseRead]
    
    class Config:
        from_attributes = True