from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime
from app.crud.base import CRUDBase
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Post]:
        result = await db.execute(
            select(Post)
            .options(selectinload(Post.author), selectinload(Post.category))
            .where(Post.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_multi_with_author(
            self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        result = await db.execute(
            select(Post)
            .options(selectinload(Post.author), selectinload(Post.category))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_published(
            self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        result = await db.execute(
            select(Post)
            .options(selectinload(Post.author), selectinload(Post.category))
            .where(Post.is_published == True)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create_with_author(
            self, db: AsyncSession, obj_in: PostCreate, author_id: int
    ) -> Post:
        db_obj = Post(
            **obj_in.model_dump(),
            author_id=author_id,
            published_at=datetime.utcnow() if obj_in.is_published else None
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def increment_view_count(self, db: AsyncSession, id: int) -> Optional[Post]:
        db_obj = await self.get(db=db, id=id)
        if not db_obj:
            return None
        db_obj.view_count += 1
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


post = CRUDPost(Post)
