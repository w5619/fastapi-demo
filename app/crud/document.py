from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.document import Document
from app.models.knowledge_base import KnowledgeBase
from app.schemas.document import DocumentCreate, DocumentUpdate

from sqlalchemy.orm import selectinload   # 用于异步预加载关联字段

# 创建文档
async def create_document(
    db: AsyncSession, 
    document: DocumentCreate
) -> Document:
    # 验证知识库是否存在
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == document.knowledge_base_id)
    )
    knowledge_base = result.scalar_one_or_none()
    
    if not knowledge_base:
        raise ValueError(f"KnowledgeBase with id {document.knowledge_base_id} does not exist")
    
    # 创建文档实例
    db_doc = Document(
        title=document.title,
        content=document.content,
        knowledge_base_id=document.knowledge_base_id
    )
    
    # 添加到数据库
    db.add(db_doc)
    await db.commit()
    await db.refresh(db_doc)
    return db_doc

# 获取单个文档
async def get_document(
    db: AsyncSession, 
    document_id: int
) -> Optional[Document]:
    result = await db.execute(
        select(Document).where(Document.id == document_id).options(selectinload(Document.knowledge_base))
    )
    return result.scalar_one_or_none()

# 获取多个文档，可按知识库筛选
async def get_documents(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    knowledge_base_id: Optional[int] = None  # 可选的知识库筛选条件
) -> List[Document]:
    query = select(Document)
    
    # 如果指定了知识库ID，添加筛选条件
    if knowledge_base_id:
        query = query.where(Document.knowledge_base_id == knowledge_base_id).options(selectinload(Document.knowledge_base))
    
    result = await db.execute(
        query.offset(skip).limit(limit)
    )
    return result.scalars().all()

# 更新文档
async def update_document(
    db: AsyncSession,
    document_id: int,
    document_update: DocumentUpdate
) -> Optional[Document]:
    # 查询要更新的文档
    result = await db.execute(
        select(Document).where(Document.id == document_id).options(selectinload(Document.knowledge_base))
    )
    db_doc = result.scalar_one_or_none()
    
    if db_doc is None:
        return None
    
    # 获取更新数据，排除未设置的字段
    update_data = document_update.model_dump(exclude_unset=True)
    # 更新字段
    for key, value in update_data.items():
        setattr(db_doc, key, value)
    
    await db.commit()
    await db.refresh(db_doc)
    return db_doc

# 删除文档
async def delete_document(
    db: AsyncSession, 
    document_id: int
) -> bool:
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    db_doc = result.scalar_one_or_none()
    
    if db_doc is None:
        return False
    
    await db.delete(db_doc)
    await db.commit()
    return True
