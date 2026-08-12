from uuid import UUID

from app.core.db import SessionDep
from app.models.users import User


def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_current_user(user_id: UUID, session: SessionDep) -> User:
    user = session.get(User, user_id)
    print(f"user {user}")
    return user


def delete_user(user: User, session: SessionDep):
    session.delete(user)
    session.commit()
