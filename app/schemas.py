from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import Priority

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.medium

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Priority] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    priority: Priority
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True