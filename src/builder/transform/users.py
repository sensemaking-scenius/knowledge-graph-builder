"""UserAccount creation from message data."""

from builder.config import user_uri
from builder.models import UserAccount


def make_user(uid: int) -> UserAccount:
    """Create a UserAccount for a Telegram user ID."""
    return UserAccount(id=user_uri(uid))
