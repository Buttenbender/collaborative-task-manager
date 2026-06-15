import pytest
from unittest.mock import MagicMock
from app.use_cases.tasks.delete_task import DeleteTask
from app.domain.entities.task import Task
from app.domain.entities.user import User

@pytest.fixture
def mock_task_repository():
    return MagicMock()

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def use_case(mock_task_repository, mock_user_repository):
    return DeleteTask(mock_task_repository, mock_user_repository)

def test_delete_task_success(use_case, mock_task_repository, mock_user_repository):
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

    use_case.execute(task_id=1)

    mock_task_repository.delete.assert_called_once_with(1)

def test_delete_task_not_found(use_case, mock_task_repository, mock_user_repository):
    mock_task_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Task not found"):
        use_case.execute(task_id=999)

    mock_task_repository.delete.assert_not_called()