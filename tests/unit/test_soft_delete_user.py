import pytest
from unittest.mock import MagicMock
from app.use_cases.users.soft_delete import SoftDeleteUser
from app.domain.entities.user import User

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def use_case(mock_repository):
    return SoftDeleteUser(mock_repository)

def test_soft_delete_user_success(use_case, mock_repository):
    mock_repository.find_by_id.return_value = User(
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

    use_case.execute(user_id=1)
    mock_repository.soft_delete.assert_called_once_with(1)

def test_soft_delete_user_not_found(use_case, mock_repository):
    mock_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="User not found"):
        use_case.execute(user_id=999)
    
    mock_repository.soft_delete.assert_not_called()