from app.domain.repositories.task_repository import TaskRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.task import Task
from app.infrastructure.logging_config import logger
from typing import Optional
from datetime import datetime

class UpdateTask:
    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self.task_repository = task_repository
        self.user_repository = user_repository
    
    def execute(self, task_id: int, title: Optional[str], description: Optional[str], due_date: Optional[datetime], status_id: Optional[int], assigned_to: Optional[int]) -> Task:
        logger.info(f"Attempting to update task - id: {task_id}")
        
        task = self.task_repository.find_by_id(task_id)
        if not task:
            logger.warning(f"Task updated failed - task not found - id: {task_id}")
            raise ValueError("Task not found")
        
        if assigned_to:
            assignee = self.user_repository.find_by_id(assigned_to)
            if not assignee:
                logger.warning(f"Task updated failed - assignee not found - id: {assigned_to}")
                raise ValueError("Assignee not found")
        
        task.title = title or task.title
        task.description = description or task.description
        task.due_date = due_date or task.due_date
        task.status_id = status_id or task.status_id
        task.assigned_to = assigned_to or task.assigned_to

        updated = self.task_repository.update(task)
        logger.info(f"Task updated successfully - id: {task_id}")
        return updated