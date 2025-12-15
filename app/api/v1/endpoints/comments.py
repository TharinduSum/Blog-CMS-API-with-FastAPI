from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import comment as crud_comment, user as crud_user, post as crud_post
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.utils.exceptions import NotFoundException, BadRequestException

router = APIRouter()


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
        comment_in: CommentCreate,
        author_id: int = Query(..., description="Author user ID"),
        db: AsyncSession = Depends(get_db)
):
    """Create a new comment"""
    # Verify author exists
    author = await crud_user.get(db=db, id=author_id)
    if not author:
        raise BadRequestException(detail="Author not found")

    # Verify post exists
    post = await crud_post.get(db=db, id=comment_in.post_id)
    if not post:
        raise BadRequestException(detail="Post not found")

    comment = await crud_comment.create_with_author(db=db, obj_in=comment_in, author_id=author_id)
    return comment


@router.get("/", response_model=List[CommentResponse])
async def read_comments(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """Retrieve all comments"""
    comments = await crud_comment.get_multi(db=db, skip=skip, limit=limit)
    return comments


@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def read_comments_by_post(
        post_id: int,
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """Get all comments for a specific post"""
    comments = await crud_comment.get_by_post(db=db, post_id=post_id, skip=skip, limit=limit)
    return comments


@router.get("/{comment_id}", response_model=CommentResponse)
async def read_comment(
        comment_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Get comment by ID"""
    comment = await crud_comment.get(db=db, id=comment_id)
    if not comment:
        raise NotFoundException(detail="Comment not found")
    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
        comment_id: int,
        comment_in: CommentUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Update a comment"""
    comment = await crud_comment.get(db=db, id=comment_id)
    if not comment:
        raise NotFoundException(detail="Comment not found")

    comment = await crud_comment.update(db=db, id=comment_id, obj_in=comment_in)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
        comment_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Delete a comment"""
    comment = await crud_comment.delete(db=db, id=comment_id)
    if not comment:
        raise NotFoundException(detail="Comment not found")
    return None
