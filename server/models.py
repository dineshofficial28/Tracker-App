from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    frequency: str = "daily"
    completed: bool = False