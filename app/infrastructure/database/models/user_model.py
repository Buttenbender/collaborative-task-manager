from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.infrastructure.database.connection import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    calendar_token = Column(String(2000), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    role = relationship("RoleModel", back_populates="users")
    tasks_owned = relationship("TaskModel", foreign_keys="TaskModel.owner_id", back_populates="owner")
    tasks_assigned = relationship("TaskModel", foreign_keys="TaskModel.assigned_to", back_populates="assignee")
    comments = relationship("CommentModel", back_populates="user")