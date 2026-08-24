from app.core.db.db import SessionDep
from app.models.collections import Collection


def create_collection(collection: Collection, session: SessionDep) -> Collection:
    session.add(collection)
    session.commit()
    session.refresh(collection)
    return collection


def delete_collection(collection: Collection, session: SessionDep):
    session.delete(collection)
    session.commit()
