from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, ARRAY
from sqlalchemy.sql import func
from ._base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import relationship

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    topic = Column(String(255), nullable=False)
    video = Column(Text, nullable=False)
    music = Column(JSON, nullable=True)
    text_effect = Column(String(100), nullable=True)
    stickers = Column(ARRAY(JSON), nullable=True)
    image_urls = Column(ARRAY(String), nullable=True)
    audio_urls = Column(ARRAY(String), nullable=True)
    subtitles = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="videos")
    
    
    @classmethod
    async def create(cls, db: AsyncSession, user_id: int, video_data: dict):
        """Create and persist a new video asynchronously."""
        video = cls(user_id=user_id, **video_data)
        db.add(video)
        try:
            await db.commit()
            await db.refresh(video)
            return video
        except IntegrityError as e:
            await db.rollback()
            print(f"IntegrityError: {e.orig}")
            return None
        
        
    @classmethod
    async def get_by_id(cls, db: AsyncSession, video_id: int):
        """Fetch a video by its ID asynchronously."""
        result = await db.execute(select(cls).filter_by(id=video_id))
        video = result.scalars().first()
        if not video:
            raise NoResultFound(f"Video with id {video_id} not found")
        return video
    
    
    @classmethod
    async def update(cls, db: AsyncSession, video_id: int, **kwargs):
        """Update a video asynchronously."""
        video = await cls.get_by_id(db, video_id)
        if not video:
            raise NoResultFound(f"Video with id {video_id} not found")
        
        for key, value in kwargs.items():
            setattr(video, key, value)
        
        try:
            await db.commit()
            await db.refresh(video)
            return video
        except IntegrityError as e:
            await db.rollback()
            print(f"IntegrityError on update: {e.orig}")
            return None
        
        
    @classmethod
    async def delete(cls, db: AsyncSession, video_id: int):
        """Delete a video asynchronously by ID."""
        result = await db.execute(select(cls).filter_by(id=video_id))
        video = result.scalars().first()
        if not video:
            raise NoResultFound(f"Video with id {video_id} not found")
        
        await db.delete(video)
        await db.commit()
        return video