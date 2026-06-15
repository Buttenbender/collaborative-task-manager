import pytest
from unittest.mock import MagicMock
from app.use_cases.tasks.create_task import CreateTask
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
    return CreateTask(mock_task_repository, mock_user_repository)

def test_create_task_success(use_case, mock_task_repository, mock_user_repository):
    mock_user_repository.find_by_id.return_value = User(
        id=1,
        name="João Büttenbender",
        email="joao@email.com",
        password_hash="hashed",
        role_id=1,
        role_name="admin",
        calendar_token=None,
        is_active=True,
        created_at=None
    )

    mock_task_repository.save.return_value = Task(
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

    result = use_case.execute(
        title="First Task",
        description="Description",
        due_date=None,
        status_id=1,
        owner_id=1,
        assigned_to=1
    )

    assert result.id == 1
    assert result.title == "First Task"
    mock_task_repository.save.assert_called_once()

def test_create_task_user_not_found(use_case, mock_task_repository, mock_user_repository):
    mock_user_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Owner not found"):
        use_case.execute(
            title="First Task",
            description="Description",
            due_date=None,
            status_id=1,
            owner_id=999,
            assigned_to=None
        )

    mock_task_repository.save.assert_not_called()

def test_create_task_assignee_not_found(use_case, mock_task_repository, mock_user_repository):
    def find_by_id_side_effect(user_id):
        if user_id == 1:
            return User(
                id=1,
                name="João Büttenbender",
                email="joao@email.com",
                password_hash="hashed",
                role_id=1,
                role_name="admin",
                calendar_token=None,
                is_active=True,
                created_at=None
            )
        return None
    
    mock_user_repository.find_by_id.side_effect = find_by_id_side_effect

    with pytest.raises(ValueError, match="Assignee not found"):
        use_case.execute(
            title="First Task",
            description="Description",
            due_date=None,
            status_id=1,
            owner_id=1,
            assigned_to=999
        )
    
    mock_task_repository.save.assert_not_called()