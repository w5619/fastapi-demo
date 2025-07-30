from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from app.crud import knowledge_base as crud_kb
from app.schemas.knowledge_base import (
    KnowledgeBaseCreate, 
    KnowledgeBaseUpdate, 
    KnowledgeBaseRead
)
from app.database import get_db

# 创建路由实例
router = APIRouter()

# 创建知识库
@router.post("/", response_model=KnowledgeBaseRead, status_code=status.HTTP_201_CREATED)
async def create_knowledge_base(
    knowledge_base: KnowledgeBaseCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建新的知识库"""
    return await crud_kb.create_knowledge_base(db=db, knowledge_base=knowledge_base)

# 获取单个知识库
@router.get("/{knowledge_base_id}", response_model=KnowledgeBaseRead)
async def read_knowledge_base(
    knowledge_base_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """根据ID获取知识库详情"""
    db_kb = await crud_kb.get_knowledge_base(db=db, knowledge_base_id=knowledge_base_id)
    if db_kb is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KnowledgeBase not found"
        )
    return db_kb

# 获取多个知识库
@router.get("/", response_model=List[KnowledgeBaseRead])
async def read_knowledge_bases(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取知识库列表，支持分页"""
    knowledge_bases = await crud_kb.get_knowledge_bases(db=db, skip=skip, limit=limit)
    return knowledge_bases

# 更新知识库
@router.put("/{knowledge_base_id}", response_model=KnowledgeBaseRead)
async def update_knowledge_base(
    knowledge_base_id: int,
    knowledge_base: KnowledgeBaseUpdate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """根据ID更新知识库"""
    db_kb = await crud_kb.update_knowledge_base(
        db=db, 
        knowledge_base_id=knowledge_base_id, 
        knowledge_base_update=knowledge_base
    )
    if db_kb is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KnowledgeBase not found"
        )
    return db_kb

# 删除知识库
@router.delete("/{knowledge_base_id}", response_model=dict)
async def delete_knowledge_base(
    knowledge_base_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """根据ID删除知识库"""
    success = await crud_kb.delete_knowledge_base(db=db, knowledge_base_id=knowledge_base_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KnowledgeBase not found"
        )
    return {"message": "KnowledgeBase deleted successfully"}
