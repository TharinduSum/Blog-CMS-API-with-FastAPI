from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.utils.exceptions import NotFoundException, BadRequestException

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_in: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    """Create a new user"""
    # Check if email exists
    existing_user = await crud_user.get_by_email(db=db, email=user_in.email)
    if existing_user:
        raise BadRequestException(detail="Email already registered")

    # Check if username exists
    existing_user = await crud_user.get_by_username(db=db, username=user_in.username)
    if existing_user:
        raise BadRequestException(detail="Username already taken")

    user = await crud_user.create(db=db, obj_in=user_in)
    return user


@router.get("/", response_model=List[UserResponse])
async def read_users(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """Retrieve all users"""
    users = await crud_user.get_multi(db=db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Get user by ID"""
    user = await crud_user.get(db=db, id=user_id)
    if not user:
        raise NotFoundException(detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
        user_id: int,
        user_in: UserUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Update a user"""
    user = await crud_user.get(db=db, id=user_id)
    if not user:
        raise NotFoundException(detail="User not found")

    # Check email uniqueness if being updated
    if user_in.email and user_in.email != user.email:
        existing_user = await crud_user.get_by_email(db=db, email=user_in.email)
        if existing_user:
            raise BadRequestException(detail="Email already registered")

    # Check username uniqueness if being updated
    if user_in.username and user_in.username != user.username:
        existing_user = await crud_user.get_by_username(db=db, username=user_in.username)
        if existing_user:
            raise BadRequestException(detail="Username already taken")

    user = await crud_user.update(db=db, id=user_id, obj_in=user_in)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Delete a user"""
    user = await crud_user.delete(db=db, id=user_id)
    if not user:
        raise NotFoundException(detail="User not found")
    return None