from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.comment import Comment

class CommentRepository(ABC):
    @abstractmethod
    def save(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def find_by_id(self, comment_id: int) -> Optional[Comment]:
        pass

    @abstractmethod
    def find_by_task_id(self, task_id: int) -> list[Comment]:
        pass

    @abstractmethod
    def delete(self, comment_id: int) -> None:
        pass