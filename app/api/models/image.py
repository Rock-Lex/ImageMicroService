from pydantic import BaseModel, Field
from datetime import datetime

class ImageOut(BaseModel):
    filename: str

class Image(BaseModel):
    filename: str
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
