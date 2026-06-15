from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must contain at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one upper case letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError("Password must contain at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one upper case letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)