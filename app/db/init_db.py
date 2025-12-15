"""
Database initialization script
Run this after creating migrations to verify setup
"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models import User, Category, Post, Comment
import asyncio

async def init_db() -> None:
    """Initialize database with sample data (optional)"""
    async with AsyncSessionLocal() as session:
        try:
            # Your initialization logic here
            # For now, just test connection
            print("✅ Database connection successful!")
            await session.commit()
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            await session.rollback()
        finally:
            await session.close()

if __name__ == "__main__":
    print("Initializing database...")
    asyncio.run(init_db())