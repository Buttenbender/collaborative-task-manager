from app.domain.repositories.comment_repository import CommentRepository
from app.infrastructure.logging_config import logger

class DeleteComment:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
    
    def execute(self, comment_id: int) -> None:
        logger.info(f"Attempting to delete comment - id: {comment_id}")

        comment = self.comment_repository.find_by_id(comment_id)
        if not comment:
            logger.warning(f"Comment deletion failed - comment not found - id: {comment_id}")
            raise ValueError("Comment not found")
        
        self.comment_repository.delete(comment_id)
        logger.info(f"Comment deleted successfully - id: {comment_id}")