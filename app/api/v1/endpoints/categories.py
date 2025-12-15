from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import category as crud_category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.utils.exceptions import NotFoundException, BadRequestException

router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
        category_in: CategoryCreate,
        db: AsyncSession = Depends(get_db)
):
    """Create a new category"""
    existing = await crud_category.get_by_slug(db=db, slug=category_in.slug)
    if existing:
        raise BadRequestException(detail="Category with this slug already exists")

    category = await crud_category.create(db=db, obj_in=category_in)
    return category


@router.get("/", response_model=List[CategoryResponse])
async def read_categories(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """Retrieve all categories"""
    categories = await crud_category.get_multi(db=db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
async def read_category(
        category_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Get category by ID"""
    category = await crud_category.get(db=db, id=category_id)
    if not category:
        raise NotFoundException(detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
        category_id: int,
        category_in: CategoryUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Update a category"""
    category = await crud_category.get(db=db, id=category_id)
    if not category:
        raise NotFoundException(detail="Category not found")

    if category_in.slug and category_in.slug != category.slug:
        existing = await crud_category.get_by_slug(db=db, slug=category_in.slug)
        if existing:
            raise BadRequestException(detail="Category with this slug already exists")

    category = await crud_category.update(db=db, id=category_id, obj_in=category_in)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Delete a category"""
    category = await crud_category.delete(db=db, id=category_id)
    if not category:
        raise NotFoundException(detail="Category not found")
    return None