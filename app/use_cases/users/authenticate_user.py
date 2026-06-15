from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.services.auth_service import create_access_token
from app.infrastructure.logging_config import logger
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthenticateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, email: str, password: str) -> str:
        logger.info(f"Login attempt with email: {email}")

        user = self.repository.find_by_email(email)
        if not user:
            logger.warning(f"Login failed - email not found: {email}")
            raise ValueError("Invalid credentials")
        
        if not pwd_context.verify(password, user.password_hash):
            logger.warning(f"Login failed - incorrect password for email: {email}")
            raise ValueError("Invalid credentials")
        
        token = create_access_token(data={"sub": str(user.id)})
        logger.info(f"Login successfull - id: {user.id}, email: {email}")
        return token