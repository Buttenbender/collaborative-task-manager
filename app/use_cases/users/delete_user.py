from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.logging_config import logger

class DeleteUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: int) -> None:
        logger.info(f"Attempting to delete user - id: {user_id}")

        user = self.repository.find_by_id(user_id)
        if not user:
            logger.warning(f"User deletion failed - user not found - id: {user_id}")
            raise ValueError("User not found")
        
        self.repository.delete(user_id)
        logger.info(f"User deleted successfully - id: {user_id}")