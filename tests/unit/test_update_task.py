import pytest
from unittest.mock import MagicMock
from app.use_cases.tasks.update_task import UpdateTask
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
    return UpdateTask(mock_task_repository, mock_user_repository)

def test_update_task_success(use_case, mock_task_repository, mock_user_repository):
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

    mock_task_repository.update.return_value = Task(
        id=1,
        title="Updated Task",
        description="Description",
        due_date=None,
        status_id=1,
        calendar_event_id=None,
        owner_id=1,
        assigned_to=1,
        created_at=None
    )

    result = use_case.execute(
        task_id=1,
        title="Updated Task",
        description=None,
        due_date=None,
        status_id=None,
        assigned_to=None
    )

    assert result.title == "Updated Task"
    mock_task_repository.update.assert_called_once()

def test_update_task_not_found(use_case, mock_task_repository, mock_user_repository):
    mock_task_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Task not found"):
        use_case.execute(
            task_id=999,
            title="Updated Task",
            description=None,
            due_date=None,
            status_id=None,
            assigned_to=None
        )

    mock_task_repository.update.assert_not_called()

def test_update_task_assignee_not_found(use_case, mock_task_repository, mock_user_repository):
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

    mock_user_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Assignee not found"):
        use_case.execute(
            task_id=1,
            title=None,
            description=None,
            due_date=None,
            status_id=None,
            assigned_to=999
        )

    mock_task_repository.update.assert_not_called()