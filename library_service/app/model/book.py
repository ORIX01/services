from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    title: str
    author: str
    published_date: Optional[datetime] = datetime.now()
    pages: int