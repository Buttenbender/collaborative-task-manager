from app.domain.entities.task import Task
from app.domain.repositories.task_repository import TaskRepository
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.services.google_calendar_service import create_calendar_event
from app.infrastructure.logging_config import logger
from typing import Optional
from datetime import datetime

class CreateTask:
    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self.task_repository = task_repository
        self.user_repository = user_repository
    
    def execute(self, title: str, description: Optional[str], due_date: Optional[datetime], status_id: int, owner_id: int, assigned_to: Optional[int]) -> Task:
        logger.info(f"Attempting to create task - owner_id: {owner_id}")

        owner = self.user_repository.find_by_id(owner_id)
        if not owner:
            logger.warning(f"Task creation failed - owner not found - id: {owner_id}")
            raise ValueError("Owner not found")
        
        if assigned_to:
            assignee = self.user_repository.find_by_id(assigned_to)
            if not assignee:
                logger.warning(f"Task creation failed - assignee not found - id: {assigned_to}")
                raise ValueError("Assignee not found")
        
        calendar_event_id = None
        if due_date and owner.calendar_token:
            try:
                calendar_event_id = create_calendar_event(
                    calendar_token=owner.calendar_token,
                    title=title,
                    due_date=due_date
                )
                logger.info(f"Google Calendar event created - event_id: {calendar_event_id}")
            except Exception as e:
                logger.error(f"Failed to create Google Calendar event: {str(e)}")
        
        task = Task(
            id=None,
            title=title,
            description=description,
            due_date=due_date,
            status_id=status_id,
            calendar_event_id=calendar_event_id,
            owner_id=owner_id,
            assigned_to=assigned_to,
            created_at=None
        )

        created = self.task_repository.save(task)
        logger.info(f"Task created successfully - id: {created.id}, title: {title}")
        return created