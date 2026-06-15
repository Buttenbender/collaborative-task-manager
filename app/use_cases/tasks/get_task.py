from app.domain.entities.task import Task
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.logging_config import logger
from typing import Optional

class GetTask:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, task_id: int) -> Task:
        logger.info(f"Attempting to get task - id: {task_id}")

        task = self.task_repository.find_by_id(task_id)
        if not task:
            logger.warning(f"Task not found - id: {task_id}")
            raise ValueError("Task not found")
        
        logger.info(f"Task retrieved successfully - id: {task_id}")
        return task
    
    def execute_all(self) -> list[Task]:
        logger.info(f"Attempting to retrieve all tasks")

        tasks = self.task_repository.find_all()
        logger.info(f"Retrieved {len(tasks)} tasks")
        return tasks
    
    def execute_with_filters(self, status_id: Optional[int], assigned_to: Optional[int]) -> list[Task]:
        logger.info(f"Attempting to retrieve tasks with filters - status_id: {status_id}, assigned_to: {assigned_to}")

        tasks = self.task_repository.find_by_filters(status_id, assigned_to)
        logger.info(f"Retrieved {len(tasks)} tasks with filters")
        return tasks