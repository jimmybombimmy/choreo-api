from app.core.db import SessionDep
from app.models.collections import Collection


def create_collection(collection: Collection, session: SessionDep) -> Collection:
    session.add(collection)
    session.commit()
    session.refresh(collection)
    return collection


def get_current_collection(user_id: Collection, session: SessionDep):
    collection = session.get(Collection, user_id)
    print(f"collection {collection}")
    return collection


def delete_user(collection: Collection, session: SessionDep):
    session.delete(collection)
    session.commit()
