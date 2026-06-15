from sqlalchemy.orm import Session
from typing import Optional
from app.domain.entities.task import Task
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.database.models.task_model import TaskModel

class MySQLTaskRepository(TaskRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, task: Task) -> Task:
        db_task = TaskModel(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status_id=task.status_id,
            calendar_event_id=task.calendar_event_id,
            owner_id=task.owner_id,
            assigned_to=task.assigned_to
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return self._to_entity(db_task)
    
    def find_by_id(self, task_id: int) -> Optional[Task]:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        return self._to_entity(db_task) if db_task else None
    
    def find_all(self) -> list[Task]:
        db_tasks = self.db.query(TaskModel).all()
        return [self._to_entity(t) for t in db_tasks]
    
    def find_by_filters(self, status_id: Optional[int], assigned_to: Optional[int]) -> list[Task]:
        query = self.db.query(TaskModel)
        if status_id:
            query = query.filter(TaskModel.status_id == status_id)
        if assigned_to:
            query = query.filter(TaskModel.assigned_to == assigned_to)
        return [self._to_entity(t) for t in query.all()]
    
    def update(self, task: Task) -> Task:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task.id).first()
        db_task.title = task.title
        db_task.description = task.description
        db_task.due_date = task.due_date
        db_task.status_id = task.status_id
        db_task.calendar_event_id = task.calendar_event_id
        db_task.assigned_to = task.assigned_to
        self.db.commit()
        self.db.refresh(db_task)
        return self._to_entity(db_task)
    
    def delete(self, task_id: int) -> None:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        self.db.delete(db_task)
        self.db.commit()
    
    def _to_entity(self, db_task: TaskModel) -> Task:
        return Task(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            due_date=db_task.due_date,
            status_id=db_task.status_id,
            calendar_event_id=db_task.calendar_event_id,
            owner_id=db_task.owner_id,
            assigned_to=db_task.assigned_to,
            created_at=db_task.created_at
        )