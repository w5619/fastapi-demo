# 从SQLAlchemy导入select查询
from sqlalchemy.future import select
# 从SQLAlchemy导入异步会话
from sqlalchemy.ext.asyncio import AsyncSession
# 从typing导入列表和可选类型
from typing import List, Optional
# 导入知识库模型
from app.models.knowledge_base import KnowledgeBase
# 导入标签模型
from app.models.tag import Tag
# 导入知识库的Pydantic模型
from app.schemas.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseUpdate

from sqlalchemy.orm import selectinload   # 用于异步预加载关联字段

# 创建知识库
async def create_knowledge_base(
    db: AsyncSession,  # 数据库会话
    knowledge_base: KnowledgeBaseCreate  # 创建知识库的数据
) -> KnowledgeBase:
    # 创建知识库实例
    db_kb = KnowledgeBase(
        name=knowledge_base.name,
        description=knowledge_base.description
    )
    
    # 如果有标签ID，关联标签
    #if knowledge_base.tag_ids:
        # 查询指定ID的标签
     #   result = await db.execute(
      #      select(Tag).where(Tag.id.in_(knowledge_base.tag_ids))
       # )
        # 将查询到的标签关联到知识库
       # db_kb.tags = result.scalars().all()

        # 如果有标签ID，处理标签关联（自动创建不存在的标签）
    if knowledge_base.tag_ids:
        # 分离已存在的ID和需要创建的ID（假设非数字ID为新标签名）
        existing_tag_ids = []
        new_tag_names = []
        
        for tag_id in knowledge_base.tag_ids:
            # 判断是否为数字ID（已存在的标签）
            if str(tag_id).isdigit():
                existing_tag_ids.append(int(tag_id))
            else:
                # 非数字视为新标签名称
                new_tag_names.append(str(tag_id))
        
        # 1. 查询已存在的标签
        existing_tags = []
        if existing_tag_ids:
            result = await db.execute(
                select(Tag).where(Tag.id.in_(existing_tag_ids))
            )
            existing_tags = result.scalars().all()
        
        # 2. 创建新标签（如果有）
        new_tags = []
        if new_tag_names:
            # 先查询是否有同名标签（避免重复创建）
            existing_name_tags = await db.execute(
                select(Tag).where(Tag.name.in_(new_tag_names))
            )
            existing_name_map = {t.name: t for t in existing_name_tags.scalars().all()}
            
            # 创建真正的新标签
            for name in new_tag_names:
                if name not in existing_name_map:
                    new_tag = Tag(name=name)
                    new_tags.append(new_tag)
                    db.add(new_tag)
            
            # 刷新会话以获取新标签的ID
            if new_tags:
                await db.flush()
        
        # 3. 合并所有标签并关联到知识库
        all_tags = existing_tags + new_tags + list(existing_name_map.values())
        db_kb.tags = all_tags
    
    # 添加到数据库
    db.add(db_kb)
    # 提交事务
    await db.commit()
    # 刷新实例，获取数据库生成的字段（如ID、创建时间）
    await db.refresh(db_kb)
    # return db_kb

    result = await db.execute(
        select(KnowledgeBase)
        .where(KnowledgeBase.id == db_kb.id)
        .options(
            selectinload(KnowledgeBase.documents),  # 预加载 documents 关联
            selectinload(KnowledgeBase.tags)       # 预加载 tags 关联
        )
    )
    return result.scalar_one()  # 返回预加载完成的对象

# 获取单个知识库
async def get_knowledge_base(
    db: AsyncSession,  # 数据库会话
    knowledge_base_id: int  # 知识库ID
) -> Optional[KnowledgeBase]:
    # 查询指定ID的知识库
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == knowledge_base_id).options(selectinload(KnowledgeBase.tags))  # 预加载tags，避免后续异步查询
    )
    # 返回查询结果，没有则返回None
    return result.scalar_one_or_none()

# 获取多个知识库
async def get_knowledge_bases(
    db: AsyncSession,  # 数据库会话
    skip: int = 0,  # 跳过前N条记录，用于分页
    limit: int = 100  # 最多返回N条记录，用于分页
) -> List[KnowledgeBase]:
    # 查询知识库，支持分页
    result = await db.execute(
        select(KnowledgeBase).offset(skip).limit(limit)
    )
    # 返回所有查询结果
    return result.scalars().all()

# 更新知识库
async def update_knowledge_base(
    db: AsyncSession,
    knowledge_base_id: int,  # 要更新的知识库ID
    knowledge_base_update: KnowledgeBaseUpdate  # 更新的数据
) -> Optional[KnowledgeBase]:
    # 查询要更新的知识库
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == knowledge_base_id)
    )
    db_kb = result.scalar_one_or_none()
    
    # 如果知识库不存在，返回None
    if db_kb is None:
        return None
    
    # 获取更新数据，排除未设置的字段
    update_data = knowledge_base_update.model_dump(exclude_unset=True)
    # 更新基本字段
    for key, value in update_data.items():
        # 跳过标签相关的字段，后面单独处理
        if key not in ["add_tag_ids", "remove_tag_ids"]:
            setattr(db_kb, key, value)
    
    # 处理添加标签
    if knowledge_base_update.add_tag_ids:
        # 查询要添加的标签
        result = await db.execute(
            select(Tag).where(Tag.id.in_(knowledge_base_update.add_tag_ids))
        )
        tags_to_add = result.scalars().all()
        # 添加标签（避免重复）
        for tag in tags_to_add:
            if tag not in db_kb.tags:
                db_kb.tags.append(tag)
    
    # 处理移除标签
    if knowledge_base_update.remove_tag_ids:
        # 过滤掉要移除的标签
        db_kb.tags = [
            tag for tag in db_kb.tags 
            if tag.id not in knowledge_base_update.remove_tag_ids
        ]
    
    # 提交事务
    await db.commit()
    # 刷新实例
    await db.refresh(db_kb)
    # return db_kb

     # 4. 关键：重新查询并预加载tags
    result = await db.execute(
        select(KnowledgeBase)
        .where(KnowledgeBase.id == db_kb.id)
        .options(selectinload(KnowledgeBase.tags))  # 强制预加载tags
    )
    return result.scalar_one()  # 返回预加载完成的对象

# 删除知识库
async def delete_knowledge_base(
    db: AsyncSession, 
    knowledge_base_id: int  # 要删除的知识库ID
) -> bool:
    # 查询要删除的知识库
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == knowledge_base_id)
    )
    db_kb = result.scalar_one_or_none()
    
    # 如果知识库不存在，返回False
    if db_kb is None:
        return False
    
    # 删除知识库
    await db.delete(db_kb)
    # 提交事务
    await db.commit()
    return True