from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, ARRAY
from sqlalchemy.sql import func
from ._base import Base

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    topic = Column(String(255), nullable=False)
    video = Column(Text, nullable=False)
    music = Column(JSON, nullable=True)
    text_effect = Column(String(100), nullable=True)
    stickers = Column(ARRAY(JSON), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())