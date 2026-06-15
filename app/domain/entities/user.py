from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    password_hash: str
    role_id: int
    role_name: Optional[str]
    calendar_token: Optional[str]
    is_active: bool
    created_at: Optional[datetime]