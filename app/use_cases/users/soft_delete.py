from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.logging_config import logger

class SoftDeleteUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, user_id: int) -> None:
        logger.info(f"Attempting to deactivate user - id: {user_id}")

        user = self.repository.find_by_id(user_id)
        if not user:
            logger.warning(f"User deactivation failed - user not found - id: {user_id}")
            raise ValueError("User not found")
        
        self.repository.soft_delete(user_id)
        logger.info(f"User deactivated successfully - id: {user_id}")