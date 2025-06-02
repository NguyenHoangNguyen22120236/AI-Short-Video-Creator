from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ._base import Base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    avatar = Column(String(255), nullable=True)
    hashed_password = Column(String(128), nullable=True)
    google_id = Column(String(100), unique=True, nullable=True)
    auth_provider = Column(String(20), nullable=True)  # e.g., 'google', 'local'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        """Create and persist a new user asynchronously."""
        user = cls(**kwargs)
        db.add(user)
        try:
            await db.commit()
            await db.refresh(user)
            return user
        except IntegrityError as e:
            await db.rollback()
            print(f"IntegrityError: {e.orig}")
            return None

    @classmethod
    async def get_by_username(cls, db: AsyncSession, username: str):
        """Fetch a user by their username asynchronously."""
        result = await db.execute(select(cls).filter_by(username=username))
        return result.scalars().first()

    @classmethod
    async def update_by_id(cls, db: AsyncSession, user_id: int, **kwargs):
        """Update a user asynchronously."""
        result = await db.execute(select(cls).filter_by(id=user_id))
        user = result.scalars().first()
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        try:
            await db.commit()
            await db.refresh(user)
            return user
        except IntegrityError as e:
            await db.rollback()
            print(f"IntegrityError on update: {e.orig}")
            return None

    @classmethod
    async def delete_by_id(cls, db: AsyncSession, user_id: int):
        """Delete a user asynchronously by ID."""
        result = await db.execute(select(cls).filter_by(id=user_id))
        user = result.scalars().first()
        if user:
            await db.delete(user)
            await db.commit()
        return user
    