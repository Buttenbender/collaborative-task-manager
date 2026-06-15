from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.mysql_task_repository import MySQLTaskRepository
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.use_cases.tasks.create_task import CreateTask
from app.use_cases.tasks.update_task import UpdateTask
from app.use_cases.tasks.delete_task import DeleteTask
from app.use_cases.tasks.get_task import GetTask
from app.adapters.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.adapters.controllers.dependencies import get_current_user, require_admin, require_user_or_admin
from app.domain.entities.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(require_user_or_admin)):
    try:
        if current_user.role_name == "user":
            if data.assigned_to != current_user.id:
                raise HTTPException(status_code=403, detail="Users can only assign tasks to themselves")
        
        use_case = CreateTask(MySQLTaskRepository(db), MySQLUserRepository(db))
        return use_case.execute(
            title=data.title,
            description=data.description,
            due_date=data.due_date,
            status_id=data.status_id,
            owner_id=current_user.id,
            assigned_to=data.assigned_to
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    status_id: Optional[int] = Query(None),
    assigned_to: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    use_case = GetTask(MySQLTaskRepository(db))
    if status_id or assigned_to:
        return use_case.execute_with_filters(status_id, assigned_to)
    return use_case.execute_all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        use_case = GetTask(MySQLTaskRepository(db))
        return use_case.execute(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_user_or_admin)):
    try:
        if current_user.role_name == "user":
            task = MySQLTaskRepository(db).find_by_id(task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            if task.owner_id != current_user.id:
                raise HTTPException(status_code=403, detail="You can only update your own tasks")
            if data.assigned_to and data.assigned_to != current_user.id:
                raise HTTPException(status_code=403, detail="Users can only assign tasks to themselves")

        use_case = UpdateTask(MySQLTaskRepository(db), MySQLUserRepository(db))
        return use_case.execute(
            task_id=task_id,
            title=data.title,
            description=data.description,
            due_date=data.due_date,
            status_id=data.status_id,
            assigned_to=data.assigned_to
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_user_or_admin)):
    try:
        if current_user.role_name == "user":
            task = MySQLTaskRepository(db).find_by_id(task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            if task.owner_id != current_user.id:
                raise HTTPException(status_code=403, detail="You can only delete your own tasks")

        use_case = DeleteTask(MySQLTaskRepository(db), MySQLUserRepository(db))
        use_case.execute(task_id)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))