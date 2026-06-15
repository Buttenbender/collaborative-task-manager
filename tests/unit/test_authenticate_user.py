import pytest
from unittest.mock import MagicMock
from app.use_cases.users.authenticate_user import AuthenticateUser
from app.domain.entities.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def use_case(mock_repository):
    return AuthenticateUser(mock_repository)

def test_authenticate_user_success(use_case, mock_repository):
    hashed = pwd_context.hash("Password123")
    mock_repository.find_by_email.return_value = User(
        id=1,
        name="João Büttenbender",
        email="joao@email.com",
        password_hash=hashed,
        role_id=1,
        role_name="admin",
        calendar_token=None,
        is_active=True,
        created_at=None
    )

    token = use_case.execute(email="joao@email.com", password="Password123")

    assert token is not None
    assert isinstance(token, str)

def test_authenticate_user_email_not_found(use_case, mock_repository):
    mock_repository.find_by_email.return_value = None

    with pytest.raises(ValueError, match="Invalid credentials"):
        use_case.execute(email="doesntexist@email.com", password="Password123")

def test_authenticate_user_wrong_password(use_case, mock_repository):
    hashed = pwd_context.hash("Password123")
    mock_repository.find_by_email.return_value = User(
        id=1,
        name="João Büttenbender",
        email="joao@email.com",
        password_hash=hashed,
        role_id=1,
        role_name="admin",
        calendar_token=None,
        is_active=True,
        created_at=None
    )

    with pytest.raises(ValueError, match="Invalid credentials"):
        use_case.execute(email="joao@email.com", password="WrongPassword1")