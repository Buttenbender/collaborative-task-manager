from app.domain.repositories.task_repository import TaskRepository
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.services.google_calendar_service import delete_calendar_event
from app.infrastructure.logging_config import logger

class DeleteTask:
    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self.task_repository = task_repository
        self.user_repository = user_repository
    
    def execute(self, task_id: int) -> None:
        logger.info(f"Attempting to delete task - id: {task_id}")

        task = self.task_repository.find_by_id(task_id)
        if not task:
            logger.warning(f"Task deletion failed - task not found - id: {task_id}")
            raise ValueError("Task not found")
        
        if task.calendar_event_id:
            owner = self.user_repository.find_by_id(task.owner_id)
            if owner and owner.calendar_token:
                try:
                    delete_calendar_event(
                        calendar_token=owner.calendar_token,
                        event_id=task.calendar_event_id
                    )
                    logger.info(f"Google Calendar event deleted - event_id: {task.calendar_event_id}")
                except Exception as e:
                    logger.error(f"Failed to delete Google Calendar event: {str(e)}")
        
        self.task_repository.delete(task_id)
        logger.info(f"Task deleted successfully - id: {task_id}")