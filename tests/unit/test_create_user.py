import pytest
from unittest.mock import MagicMock
from app.use_cases.users.create_user import CreateUser
from app.domain.entities.user import User

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def use_case(mock_repository):
    return CreateUser(mock_repository)

def test_create_user_success(use_case, mock_repository):
    mock_repository.find_by_email.return_value = None
    mock_repository.save.return_value = User(
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

    result = use_case.execute(
        name="João Büttenbender",
        email="joao@email.com",
        password="Password123",
        role_id=1
    )

    assert result.id == 1
    assert result.email == "joao@email.com"
    mock_repository.save.assert_called_once()

def test_create_user_duplicate_email(use_case, mock_repository):
    mock_repository.find_by_email.return_value = User(
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

    with pytest.raises(ValueError, match="E-mail already registered"):
        use_case.execute(
            name="João Büttenbender",
            email="joao@email.com",
            password="Password123",
            role_id=1
        )

    mock_repository.save.assert_not_called()

def test_create_user_password_is_hashed(use_case, mock_repository):
    mock_repository.find_by_email.return_value = None
    mock_repository.save.return_value = User(
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

    use_case.execute(
        name="João Büttenbender",
        email="joao@email.com",
        password="Password123",
        role_id=1
    )

    saved_user = mock_repository.save.call_args[0][0]
    assert saved_user.password_hash != "Password123"