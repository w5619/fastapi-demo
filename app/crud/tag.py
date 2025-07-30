from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate

# 创建标签
async def create_tag(
    db: AsyncSession, 
    tag: TagCreate
) -> Tag:
    # 检查标签名称是否已存在
    result = await db.execute(
        select(Tag).where(Tag.name == tag.name)
    )
    existing_tag = result.scalar_one_or_none()
    
    if existing_tag:
        raise ValueError(f"Tag with name '{tag.name}' already exists")
    
    # 创建标签实例
    db_tag = Tag(
        name=tag.name,
        color=tag.color
    )
    
    # 添加到数据库
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

# 获取单个标签
async def get_tag(
    db: AsyncSession, 
    tag_id: int
) -> Optional[Tag]:
    result = await db.execute(
        select(Tag).where(Tag.id == tag_id)
    )
    return result.scalar_one_or_none()

# 通过名称获取标签
async def get_tag_by_name(
    db: AsyncSession, 
    name: str
) -> Optional[Tag]:
    result = await db.execute(
        select(Tag).where(Tag.name == name)
    )
    return result.scalar_one_or_none()

# 获取多个标签
async def get_tags(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[Tag]:
    result = await db.execute(
        select(Tag).offset(skip).limit(limit)
    )
    return result.scalars().all()

# 更新标签
async def update_tag(
    db: AsyncSession,
    tag_id: int,
    tag_update: TagUpdate
) -> Optional[Tag]:
    # 查询要更新的标签
    result = await db.execute(
        select(Tag).where(Tag.id == tag_id)
    )
    db_tag = result.scalar_one_or_none()
    
    if db_tag is None:
        return None
    
    # 如果更新了名称，检查新名称是否已存在
    if tag_update.name and tag_update.name != db_tag.name:
        existing_tag = await get_tag_by_name(db, tag_update.name)
        if existing_tag:
            raise ValueError(f"Tag with name '{tag_update.name}' already exists")
    
    # 获取更新数据，排除未设置的字段
    update_data = tag_update.model_dump(exclude_unset=True)
    # 更新字段
    for key, value in update_data.items():
        setattr(db_tag, key, value)
    
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

# 删除标签
async def delete_tag(
    db: AsyncSession, 
    tag_id: int
) -> bool:
    result = await db.execute(
        select(Tag).where(Tag.id == tag_id)
    )
    db_tag = result.scalar_one_or_none()
    
    if db_tag is None:
        return False
    
    await db.delete(db_tag)
    await db.commit()
    return True
