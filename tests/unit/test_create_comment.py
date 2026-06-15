import pytest
from unittest.mock import MagicMock
from app.use_cases.comments.create_comment import CreateComment
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
    return CreateComment(mock_comment_repository, mock_task_repository)

def test_create_comment_success(use_case, mock_comment_repository, mock_task_repository):
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
    mock_comment_repository.save.return_value = Comment(
        id=1,
        content="First comment!",
        task_id=1,
        user_id=1,
        created_at=None
    )

    result = use_case.execute(content="First comment!", task_id=1, user_id=1)

    assert result.id == 1
    assert result.content == "First comment!"
    mock_comment_repository.save.assert_called_once()

def test_create_comment_task_not_found(use_case, mock_comment_repository, mock_task_repository):
    mock_task_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Task not found"):
        use_case.execute(content="First comment!", task_id=999, user_id=1)

    mock_comment_repository.save.assert_not_called()