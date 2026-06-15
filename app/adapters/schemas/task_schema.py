from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status_id: int
    assigned_to: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status_id: Optional[int] = None
    assigned_to: Optional[int] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    status_id: int
    calendar_event_id: Optional[str]
    owner_id: int
    assigned_to: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)