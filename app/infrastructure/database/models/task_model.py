from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.infrastructure.database.connection import Base

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    status_id = Column(Integer, ForeignKey("statuses.id"), nullable=False)
    calendar_event_id = Column(String(255), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    status = relationship("StatusModel", back_populates="tasks")
    owner = relationship("UserModel", foreign_keys=[owner_id], back_populates="tasks_owned")
    assignee = relationship("UserModel", foreign_keys=[assigned_to], back_populates="tasks_assigned")
    comments = relationship("CommentModel", back_populates="task")