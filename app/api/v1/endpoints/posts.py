from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import post as crud_post, user as crud_user
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.utils.exceptions import NotFoundException, BadRequestException

router = APIRouter()


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
        post_in: PostCreate,
        author_id: int = Query(..., description="Author user ID"),
        db: AsyncSession = Depends(get_db)
):
    """Create a new post"""
    # Verify author exists
    author = await crud_user.get(db=db, id=author_id)
    if not author:
        raise BadRequestException(detail="Author not found")

    # Check if slug exists
    existing = await crud_post.get_by_slug(db=db, slug=post_in.slug)
    if existing:
        raise BadRequestException(detail="Post with this slug already exists")

    post = await crud_post.create_with_author(db=db, obj_in=post_in, author_id=author_id)
    return post


@router.get("/", response_model=List[PostResponse])
async def read_posts(
        skip: int = 0,
        limit: int = 100,
        published_only: bool = False,
        db: AsyncSession = Depends(get_db)
):
    """Retrieve all posts"""
    if published_only:
        posts = await crud_post.get_published(db=db, skip=skip, limit=limit)
    else:
        posts = await crud_post.get_multi_with_author(db=db, skip=skip, limit=limit)
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def read_post(
        post_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Get post by ID"""
    post = await crud_post.get(db=db, id=post_id)
    if not post:
        raise NotFoundException(detail="Post not found")

    # Increment view count
    await crud_post.increment_view_count(db=db, id=post_id)
    return post


@router.get("/slug/{slug}", response_model=PostResponse)
async def read_post_by_slug(
        slug: str,
        db: AsyncSession = Depends(get_db)
):
    """Get post by slug"""
    post = await crud_post.get_by_slug(db=db, slug=slug)
    if not post:
        raise NotFoundException(detail="Post not found")

    # Increment view count
    await crud_post.increment_view_count(db=db, id=post.id)
    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
        post_id: int,
        post_in: PostUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Update a post"""
    post = await crud_post.get(db=db, id=post_id)
    if not post:
        raise NotFoundException(detail="Post not found")

    # Check slug uniqueness if being updated
    if post_in.slug and post_in.slug != post.slug:
        existing = await crud_post.get_by_slug(db=db, slug=post_in.slug)
        if existing:
            raise BadRequestException(detail="Post with this slug already exists")

    post = await crud_post.update(db=db, id=post_id, obj_in=post_in)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Delete a post"""
    post = await crud_post.delete(db=db, id=post_id)
    if not post:
        raise NotFoundException(detail="Post not found")
    return None
