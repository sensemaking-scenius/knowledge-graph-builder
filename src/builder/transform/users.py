"""UserAccount creation from message data."""

from builder.config import user_uri
from builder.models import UserAccount


def make_user(
    uid: int,
    name: str | None = None,
    username: str | None = None,
    is_bot: bool | None = None,
    is_verified: bool | None = None,
    is_premium: bool | None = None,
) -> UserAccount:
    """Create a UserAccount for a Telegram user ID."""
    return UserAccount(
        id=user_uri(uid),
        name=name,
        username=username,
        is_bot=is_bot if is_bot else None,
        is_verified=is_verified if is_verified else None,
        is_premium=is_premium if is_premium else None,
    )
