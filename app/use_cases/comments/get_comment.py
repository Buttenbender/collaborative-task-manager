from app.domain.entities.comment import Comment
from app.domain.repositories.comment_repository import CommentRepository
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.logging_config import logger

class GetComment:
    def __init__(self, comment_repository: CommentRepository, task_repository: TaskRepository):
        self.comment_repository = comment_repository
        self.task_repository = task_repository
    
    def execute_by_task(self, task_id: int) -> list[Comment]:
        logger.info(f"Attempting to retrieve comments - task_id: {task_id}")

        task = self.task_repository.find_by_id(task_id)
        if not task:
            logger.warning(f"Comment retrieval failed - task not found - id: {task_id}")
            raise ValueError("Task not found")
        
        comments = self.comment_repository.find_by_task_id(task_id)
        logger.info(f"Retrieve {len(comments)} comments - task_id: {task_id}")
        return comments