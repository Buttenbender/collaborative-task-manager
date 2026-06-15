from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.task import Task

class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task:
        pass

    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def find_all(self) -> list[Task]:
        pass

    @abstractmethod
    def find_by_filters(self, status_id: Optional[int], assigned_to: Optional[int]) -> list[Task]:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        pass