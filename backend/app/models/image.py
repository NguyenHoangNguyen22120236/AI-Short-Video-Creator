from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ._base import Base

class Image(Base):
    __tablename__ = 'images'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey('videos.video_id'), nullable=False, index=True)
    ordered_number = Column(Integer, nullable=False)    
    image_url = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())