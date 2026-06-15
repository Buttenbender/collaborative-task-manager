from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.services.auth_service import verify_token
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.infrastructure.logging_config import logger
from app.domain.entities.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = verify_token(token)
    if not payload:
        logger.warning("Authentication failed - invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user_id = int(payload.get("sub"))
    user = MySQLUserRepository(db).find_by_id(user_id)
    if not user:
        logger.warning(f"Authentication failed - user not found - id: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    logger.info(f"User authenticated successfully - id: {user_id}")
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role_name != "admin":
        logger.warning(f"Access denied = user is not admin - id: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to asministrators"
        )
    return current_user

def require_user_or_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role_name not in ["admin", "user"]:
        logger.warning(f"Access denied - insufficient permissions - id: {current_user.id}, role: {current_user.role_name}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to users and administrators"
        )
    return current_user