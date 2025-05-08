from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ._base import Base

class Video(Base):
    __tablename__ = 'videos'

    video_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    topic = Column(String(255), nullable=False)
    video_url = Column(Text, nullable=False)
    background_music_url = Column(Text, nullable=True)
    text_effect = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())