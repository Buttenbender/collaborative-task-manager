from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.logging_config import logger
from typing import Optional

class GetUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, user_id: int) -> Optional[User]:
        logger.info(f"Attempting to get user - id: {user_id}")

        user = self.repository.find_by_id(user_id)
        if not user:
            logger.warning(f"User not found - id: {user_id}")
            raise ValueError("User not found")
        logger.info(f"User retrieved successfully - id: {user_id}")
        return user
    
    def execute_all(self) -> list[User]:
        logger.info(f"Attempting to retrieve all users")
        users = self.repository.find_all()
        logger.info(f"Retrieved {len(users)} users")
        return users