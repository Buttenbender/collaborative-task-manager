from sqlalchemy.orm import Session
from typing import Optional
from app.domain.entities.comment import Comment
from app.domain.repositories.comment_repository import CommentRepository
from app.infrastructure.database.models.comment_model import CommentModel

class MySQLCommentRepository(CommentRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, comment: Comment) -> Comment:
        db_comment = CommentModel(
            content=comment.content,
            task_id=comment.task_id,
            user_id=comment.user_id
        )
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return self._to_entity(db_comment)
    
    def find_by_id(self, comment_id: int) -> Optional[Comment]:
        db_comment = self.db.query(CommentModel).filter(CommentModel.id == comment_id).first()
        return self._to_entity(db_comment) if db_comment else None
    
    def find_by_task_id(self, task_id: int) -> list[Comment]:
        db_comment = self.db.query(CommentModel).filter(CommentModel.task_id == task_id).all()
        return [self._to_entity(c) for c in db_comment]
    
    def delete(self, comment_id: int) -> None:
        db_comment = self.db.query(CommentModel).filter(CommentModel.id == comment_id).first()
        self.db.delete(db_comment)
        self.db.commit()
    
    def _to_entity(self, db_comment: CommentModel) -> Comment:
        return Comment(
            id=db_comment.id,
            content=db_comment.content,
            task_id=db_comment.task_id,
            user_id=db_comment.user_id,
            created_at=db_comment.created_at
        )