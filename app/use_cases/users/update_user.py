from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.logging_config import logger
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UpdateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, user_id: int, name: Optional[str], email: Optional[str], password: Optional[str], role_id: Optional[int]) -> User:
        logger.info(f"Attempting to update user - id: {user_id}")
        
        user = self.repository.find_by_id(user_id)
        if not user:
            logger.warning(f"User update failed - user not found - id: {user_id}")
            raise ValueError("User not found")
        
        if email and email != user.email:
            existing = self.repository.find_by_email(email)
            if existing:
                logger.warning(f"User update failed - email already registered: {email}")
                raise ValueError("Email already registered")
            
        user.name = name or user.name
        user.email = email or user.email
        user.role_id = role_id or user.role_id

        if password:
            user.password_hash = pwd_context.hash(password)
        
        updated = self.repository.update(user)
        logger.info(f"User updated successfully - id: {user_id}")
        return updated