from uuid import UUID
from sqlalchemy.exc import NoResultFound

from app.core.db.db import SessionDep
from app.models.users import User


def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(user_id: UUID, session: SessionDep):
    retrieved_user = session.get(User, user_id)
    if retrieved_user == None:
        raise NoResultFound(f"User Not Found")
    return retrieved_user


def delete_user(user_id: UUID, session: SessionDep):
    user = get_user_by_id(user_id, session)
    session.delete(user)
    session.commit()
