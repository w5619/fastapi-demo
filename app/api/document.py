from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any, Optional
from app.crud import document as crud_doc
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentRead
from app.database import get_db

# 创建路由实例
router = APIRouter()

# 创建文档
@router.post("/", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def create_document(
    document: DocumentCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """创建新的文档"""
    try:
        return await crud_doc.create_document(db=db, document=document)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail = None
        )

# 获取单个文档
@router.get("/{document_id}", response_model=DocumentRead)
async def read_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """根据ID获取文档详情"""
    db_doc = await crud_doc.get_document(db=db, document_id=document_id)
    if db_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return db_doc

# 获取多个文档
@router.get("/", response_model=List[DocumentRead])
async def read_documents(
    skip: int = 0,
    limit: int = 100,
    knowledge_base_id: Optional[int] = None,  # 可选的知识库筛选参数
    db: AsyncSession = Depends(get_db)
) -> Any:
    """获取文档列表，支持分页和按知识库筛选"""
    documents = await crud_doc.get_documents(
        db=db, 
        skip=skip, 
        limit=limit,
        knowledge_base_id=knowledge_base_id
    )
    return documents

# 更新文档
@router.put("/{document_id}", response_model=DocumentRead)
async def update_document(
    document_id: int,
    document: DocumentUpdate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """根据ID更新文档"""
    db_doc = await crud_doc.update_document(
        db=db, 
        document_id=document_id, 
        document_update=document
    )
    if db_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return db_doc

# 删除文档
@router.delete("/{document_id}", response_model=dict)
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """根据ID删除文档"""
    success = await crud_doc.delete_document(db=db, document_id=document_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return {"message": "Document deleted successfully"}
