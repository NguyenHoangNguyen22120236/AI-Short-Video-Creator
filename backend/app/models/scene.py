from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.sql import func
from ._base import Base

class Scene(Base):
    __tablename__ = 'scenes'

    scence_id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey('videos.video_id'), nullable=False, index=True)
    ordered_number = Column(Integer, nullable=False)    
    subtitles = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())