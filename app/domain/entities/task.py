from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: Optional[int]
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    status_id: int
    calendar_event_id: Optional[str]
    owner_id: int
    assigned_to: Optional[int]
    created_at: Optional[datetime]