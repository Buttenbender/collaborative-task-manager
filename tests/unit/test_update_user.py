import pytest
from unittest.mock import MagicMock
from app.use_cases.users.update_user import UpdateUser
from app.domain.entities.user import User

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def use_case(mock_repository):
    return UpdateUser(mock_repository)

def test_update_user_success(use_case, mock_repository):
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

    mock_repository.update.return_value = User(
        id=1,
        name="João Updated",
        email="joao@email.com",
        password_hash="hashed",
        role_id=1,
        role_name="admin",
        calendar_token=None,
        is_active=True,
        created_at=None
    )

    result = use_case.execute(
        user_id=1,
        name="João Updated",
        email=None,
        password=None,
        role_id=None
    )

    assert result.name == "João Updated"
    mock_repository.update.assert_called_once()

def test_update_user_not_found(use_case, mock_repository):
    mock_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="User not found"):
        use_case.execute(
            user_id=999,
            name="João Updated",
            email=None,
            password=None,
            role_id=None
        )

def test_update_duplicate_email(use_case, mock_repository):
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

    mock_repository.find_by_email.return_value = User(
        id=2,
        name="Other User",
        email="other@email.com",
        password_hash="hashed",
        role_id=1,
        role_name="admin",
        calendar_token=None,
        is_active=True,
        created_at=None
    )

    with pytest.raises(ValueError, match="Email already registered"):
        use_case.execute(
            user_id=1,
            name=None,
            email="other@email.com",
            password=None,
            role_id=None
        )