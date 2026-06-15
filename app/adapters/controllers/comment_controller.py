from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.mysql_comment_repository import MySQLCommentRepository
from app.infrastructure.repositories.mysql_task_repository import MySQLTaskRepository
from app.use_cases.comments.create_comment import CreateComment
from app.use_cases.comments.delete_comment import DeleteComment
from app.use_cases.comments.get_comment import GetComment
from app.adapters.schemas.comment_schema import CommentCreate, CommentResponse
from app.adapters.controllers.dependencies import get_current_user, require_admin, require_user_or_admin
from app.domain.entities.user import User

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["Comments"])

@router.post("/", response_model=CommentResponse, status_code=201)
def create_comment(task_id: int, data: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_user_or_admin)):
    try:
        use_case = CreateComment(MySQLCommentRepository(db), MySQLTaskRepository(db))
        return use_case.execute(
            content=data.content,
            task_id=task_id,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=list[CommentResponse])
def get_comments(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        use_case = GetComment(MySQLCommentRepository(db), MySQLTaskRepository(db))
        return use_case.execute_by_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{comment_id}", status_code=204)
def delete_comment(task_id: int, comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_user_or_admin)):
    try:
        if current_user.role_name == "user":
            comment = MySQLCommentRepository(db).find_by_id(comment_id)
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
            if comment.user_id != current_user.id:
                raise HTTPException(status_code=403, detail="You can only delete your own comments")

        use_case = DeleteComment(MySQLCommentRepository(db))
        use_case.execute(comment_id)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))