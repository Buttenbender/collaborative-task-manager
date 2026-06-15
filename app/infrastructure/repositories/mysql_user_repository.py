from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel
from typing import Optional

class MySQLUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, user: User) -> User:
        db_user = UserModel(
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            role_id=user.role_id,
            calendar_token=user.calendar_token,
            is_active=True
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_active == True).first()
        return self._to_entity(db_user) if db_user else None
    
    def find_by_email(self, email: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.email == email, UserModel.is_active == True).first()
        return self._to_entity(db_user) if db_user else None
    
    def find_all(self) -> list[User]:
        db_users = self.db.query(UserModel).filter(UserModel.is_active == True).all()
        return [self._to_entity(u) for u in db_users]
    
    def update(self, user: User) -> User:
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        db_user.name = user.name
        db_user.email = user.email
        db_user.password_hash = user.password_hash
        db_user.role_id = user.role_id
        db_user.calendar_token = user.calendar_token
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)
    
    def delete(self, user_id: int) -> None:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        self.db.delete(db_user)
        self.db.commit()

    def soft_delete(self, user_id: int) -> None:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        db_user.is_active = False
        self.db.commit()
    
    def _to_entity(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password_hash=db_user.password_hash,
            role_id=db_user.role_id,
            role_name=db_user.role.name if db_user.role else None,
            calendar_token=db_user.calendar_token,
            is_active=db_user.is_active,
            created_at=db_user.created_at
        )