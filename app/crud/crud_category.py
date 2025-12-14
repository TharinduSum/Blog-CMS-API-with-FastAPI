from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Category]:
        result = await db.execute(select(Category).where(Category.slug == slug))
        return result.scalar_one_or_none()

category = CRUDCategory(Category)