import pytest
from unittest.mock import MagicMock
from app.use_cases.comments.delete_comment import DeleteComment
from app.domain.entities.comment import Comment

@pytest.fixture
def mock_comment_repository():
    return MagicMock()

@pytest.fixture
def use_case(mock_comment_repository):
    return DeleteComment(mock_comment_repository)

def test_delete_comment_success(use_case, mock_comment_repository):
    mock_comment_repository.find_by_id.return_value = Comment(
        id=1,
        content="First comment!",
        task_id=1,
        user_id=1,
        created_at=None
    )

    use_case.execute(comment_id=1)

    mock_comment_repository.delete.assert_called_once_with(1)

def test_delete_comment_not_found(use_case, mock_comment_repository):
    mock_comment_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Comment not found"):
        use_case.execute(comment_id=999)

    mock_comment_repository.delete.assert_not_called()