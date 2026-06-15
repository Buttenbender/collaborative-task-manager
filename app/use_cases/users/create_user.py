from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.logging_config import logger
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, name: str, email: str, password: str, role_id: int) -> User:
        logger.info(f"Attempting to create user with email: {email}")

        existing_user = self.repository.find_by_email(email)
        if existing_user:
            logger.warning(f"User creation failed - email already registered: {email}")
            raise ValueError("E-mail already registered")
        
        password_hash = pwd_context.hash(password)

        user = User(
            id=None,
            name=name,
            email=email,
            password_hash=password_hash,
            role_id=role_id,
            role_name=None,
            calendar_token=None,
            is_active=True,
            created_at=None
        )

        created = self.repository.save(user)
        logger.info(f"User created successfully - id: {created.id}, email: {email}")
        return created