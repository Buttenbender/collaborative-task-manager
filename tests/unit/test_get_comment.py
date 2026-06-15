import pytest
from unittest.mock import MagicMock
from app.use_cases.comments.get_comment import GetComment
from app.domain.entities.comment import Comment
from app.domain.entities.task import Task

@pytest.fixture
def mock_comment_repository():
    return MagicMock()

@pytest.fixture
def mock_task_repository():
    return MagicMock()

@pytest.fixture
def use_case(mock_comment_repository, mock_task_repository):
    return GetComment(mock_comment_repository, mock_task_repository)

def test_get_comments_by_task_success(use_case, mock_comment_repository, mock_task_repository):
    mock_task_repository.find_by_id.return_value = Task(
        id=1,
        title="First Task",
        description="Description",
        due_date=None,
        status_id=1,
        calendar_event_id=None,
        owner_id=1,
        assigned_to=1,
        created_at=None
    )
    mock_comment_repository.find_by_task_id.return_value = [
        Comment(
            id=1, 
            content="First comment!", 
            task_id=1, 
            user_id=1, 
            created_at=None
        ),
        Comment(
            id=2, 
            content="Second comment!", 
            task_id=1, 
            user_id=1, 
            created_at=None
        )
    ]

    result = use_case.execute_by_task(task_id=1)

    assert len(result) == 2
    mock_comment_repository.find_by_task_id.assert_called_once_with(1)

def test_get_comments_task_not_found(use_case, mock_comment_repository, mock_task_repository):
    mock_task_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Task not found"):
        use_case.execute_by_task(task_id=999)

    mock_comment_repository.find_by_task_id.assert_not_called()