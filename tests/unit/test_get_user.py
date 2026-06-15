import pytest
from unittest.mock import MagicMock
from app.use_cases.users.get_user import GetUser
from app.domain.entities.user import User

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def use_case(mock_repository):
    return GetUser(mock_repository)

def test_get_user_success(use_case, mock_repository):
    mock_repository.find_by_id.return_value = User(
        id=1,
        name="João Silva",
        email="joao@email.com",
        password_hash="hashed",
        role_id=1,
        role_name="admin",
        calendar_token=None,
        is_active=True,
        created_at=None
    )

    result = use_case.execute(user_id=1)

    assert result.id == 1
    assert result.email == "joao@email.com"

def test_get_user_not_found(use_case, mock_repository):
    mock_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="User not found"):
        use_case.execute(user_id=999)

def test_get_all_users(use_case, mock_repository):
    mock_repository.find_all.return_value = [
        User(
            id=1, 
            name="João Büttenbender", 
            email="joao@email.com", 
            password_hash="hashed", 
            role_id=1, 
            role_name="admin", 
            calendar_token=None, 
            is_active=True, 
            created_at=None
        ),
        User(
            id=2, 
            name="Alexia Ferreira", 
            email="alexia@email.com", 
            password_hash="hashed", 
            role_id=2, 
            role_name="user", 
            calendar_token=None, 
            is_active=True, 
            created_at=None
        )
    ]

    result = use_case.execute_all()

    assert len(result) == 2