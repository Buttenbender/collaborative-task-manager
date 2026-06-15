from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.use_cases.users.create_user import CreateUser
from app.use_cases.users.update_user import UpdateUser
from app.use_cases.users.delete_user import DeleteUser
from app.use_cases.users.soft_delete import SoftDeleteUser
from app.use_cases.users.get_user import GetUser
from app.adapters.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.domain.entities.user import User
from app.adapters.controllers.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        use_case = CreateUser(MySQLUserRepository(db))
        return use_case.execute(
            name=data.name,
            email=data.email,
            password=data.password,
            role_id=data.role_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    use_case = GetUser(MySQLUserRepository(db))
    return use_case.execute_all()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        use_case = GetUser(MySQLUserRepository(db))
        return use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        use_case = UpdateUser(MySQLUserRepository(db))
        return use_case.execute(
            user_id=user_id,
            name=data.name,
            email=data.email,
            password=data.password,
            role_id=data.role_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        use_case = DeleteUser(MySQLUserRepository(db))
        use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}/deactivate", status_code=204)
def soft_delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        use_case = SoftDeleteUser(MySQLUserRepository(db))
        use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))