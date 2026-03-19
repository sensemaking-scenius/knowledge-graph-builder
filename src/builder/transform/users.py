"""User + Person creation from participant data."""

from builder.config import person_uri, user_uri
from builder.models import Person, User


def make_user(
    uid: int,
    name: str | None = None,
    username: str | None = None,
    is_bot: bool | None = None,
) -> User:
    """Create a User for a Telegram user ID."""
    return User(
        id=user_uri(uid),
        sioc_name=name,
        username=username,
        is_bot=is_bot if is_bot else None,
        account_of=person_uri(uid),
    )


def make_person(uid: int, name: str | None = None) -> Person:
    """Create a Person linked to a User."""
    return Person(
        id=person_uri(uid),
        name=name,
        holds_account=[user_uri(uid)],
    )
