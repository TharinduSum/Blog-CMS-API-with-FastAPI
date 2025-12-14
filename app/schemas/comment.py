from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.user import UserResponse


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)
    post_id: int
    parent_id: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)
    is_approved: Optional[bool] = None


class CommentResponse(CommentBase):
    id: int
    is_approved: bool
    author_id: int
    created_at: datetime
    updated_at: datetime
    author: Optional[UserResponse] = None

    class Config:
        from_attributes = True