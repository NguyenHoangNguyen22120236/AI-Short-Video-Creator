from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ._base import Base

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