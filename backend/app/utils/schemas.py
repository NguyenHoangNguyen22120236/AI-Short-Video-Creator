from pydantic import BaseModel
from typing import Optional, List

class VideoSchema(BaseModel):
    id: int
    video: str
    text_effect: Optional[str]
    music: Optional[dict]
    stickers: Optional[List[dict]]

    class Config:
        orm_mode = True