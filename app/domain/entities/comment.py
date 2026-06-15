from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Comment:
    id: Optional[int]
    content: str
    task_id: int
    user_id: int
    created_at: Optional[datetime]