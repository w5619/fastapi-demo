from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from app.crud import tag as crud_tag
from app.schemas.tag import TagCreate, TagUpdate, TagRead
from app.database import get_db

# 创建路由实例
router = APIRouter()

# 创建标签
@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag: TagCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建新的标签"""
    try:
        return await crud_tag.create_tag(db=db, tag=tag)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# 获取单个标签
@router.get("/{tag_id}", response_model=TagRead)
async def read_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """根据ID获取标签详情"""
    db_tag = await crud_tag.get_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return db_tag

# 获取多个标签
@router.get("/", response_model=List[TagRead])
async def read_tags(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取标签列表，支持分页"""
    tags = await crud_tag.get_tags(db=db, skip=skip, limit=limit)
    return tags

# 更新标签
@router.put("/{tag_id}", response_model=TagRead)
async def update_tag(
    tag_id: int,
    tag: TagUpdate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """根据ID更新标签"""
    try:
        db_tag = await crud_tag.update_tag(
            db=db, 
            tag_id=tag_id, 
            tag_update=tag
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return db_tag

# 删除标签
@router.delete("/{tag_id}", response_model=dict)
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """根据ID删除标签"""
    success = await crud_tag.delete_tag(db=db, tag_id=tag_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return {"message": "Tag deleted successfully"}
