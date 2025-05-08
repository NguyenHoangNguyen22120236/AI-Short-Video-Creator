from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ._base import Base

class Sticker(Base):
    __tablename__ = 'stickers'

    sticker_id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey('videos.video_id'), nullable=False, index=True)
    sticker_url = Column(Text, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())