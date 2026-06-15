from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.use_cases.users.authenticate_user import AuthenticateUser
from app.adapters.schemas.auth_schema import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        use_case = AuthenticateUser(MySQLUserRepository(db))
        token = use_case.execute(email=data.email, password=data.password)
        return TokenResponse(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout", status_code=204)
def logout():
    return None