from app.domain.entities.comment import Comment
from app.domain.repositories.comment_repository import CommentRepository
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.logging_config import logger

class CreateComment:
    def __init__(self, comment_repository: CommentRepository, task_repository: TaskRepository):
        self.comment_repository = comment_repository
        self.task_repository = task_repository
    
    def execute(self, content: str, task_id: int, user_id: int) -> Comment:
        logger.info(f"Attempting to create comment - task_id: {task_id}, user_id: {user_id}")

        task = self.task_repository.find_by_id(task_id)
        if not task:
            logger.warning(f"Comment creation failed - task not found - id: {task_id}")
            raise ValueError("Task not found")
        
        comment = Comment(
            id=None,
            content=content,
            task_id=task_id,
            user_id=user_id,
            created_at=None
        )

        created = self.comment_repository.save(comment)
        logger.info(f"Comment created successfully - id: {created.id}, task_id: {task_id}")
        return created