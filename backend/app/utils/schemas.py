from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class VideoSchema(BaseModel):
    id: int
    video: str
    topic: str
    text_effect: Optional[str]
    music: Optional[dict]
    stickers: Optional[List[dict]]
    thumbnail: str

    class Config:
        orm_mode = True
        
class VideoHistorySchema(BaseModel):
    id: int
    topic: str
    created_at: datetime
    thumbnail: str

    class Config:
        orm_mode = True