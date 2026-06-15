import pytest
from unittest.mock import MagicMock
from app.use_cases.tasks.get_task import GetTask
from app.domain.entities.task import Task

@pytest.fixture
def mock_task_repository():
    return MagicMock()

@pytest.fixture
def use_case(mock_task_repository):
    return GetTask(mock_task_repository)

def test_get_task_success(use_case, mock_task_repository):
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

    result = use_case.execute(task_id=1)

    assert result.id == 1
    assert result.title == "First Task"

def test_get_task_not_found(use_case, mock_task_repository):
    mock_task_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Task not found"):
        use_case.execute(task_id=999)

def test_get_all_tasks(use_case, mock_task_repository):
    mock_task_repository.find_all.return_value = [
        Task(
            id=1,
            title="First Task",
            description="Description",
            due_date=None,
            status_id=1,
            calendar_event_id=None,
            owner_id=1,
            assigned_to=1,
            created_at=None
        ),
        Task(
            id=2,
            title="Second Task",
            description="Description",
            due_date=None,
            status_id=1,
            calendar_event_id=None,
            owner_id=1,
            assigned_to=1,
            created_at=None
        )
    ]

    result = use_case.execute_all()

    assert len(result) == 2

def test_get_tasks_with_filters(use_case, mock_task_repository):
    mock_task_repository.find_by_filters.return_value = [
        Task(
            id=1, 
            title="First Task", 
            description="Description", 
            due_date=None, status_id=1, 
            calendar_event_id=None, 
            owner_id=1, 
            assigned_to=1, 
            created_at=None
        )
    ]

    result = use_case.execute_with_filters(status_id=1, assigned_to=None)

    assert len(result) == 1
    mock_task_repository.find_by_filters.assert_called_once_with(1, None)