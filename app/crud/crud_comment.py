from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.crud.base import CRUDBase
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    async def get_by_post(
            self, db: AsyncSession, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        result = await db.execute(
            select(Comment)
            .options(selectinload(Comment.author))
            .where(Comment.post_id == post_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create_with_author(
            self, db: AsyncSession, obj_in: CommentCreate, author_id: int
    ) -> Comment:
        db_obj = Comment(**obj_in.model_dump(), author_id=author_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


comment = CRUDComment(Comment)