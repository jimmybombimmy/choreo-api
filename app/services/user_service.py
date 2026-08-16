from app.core.db import SessionDep
from app.models.users import User


def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(user: User, session: SessionDep):
    session.delete(user)
    session.commit()
