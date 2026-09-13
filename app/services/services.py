from uuid import UUID

from sqlalchemy.exc import NoResultFound

from app.core.db import SessionDep
from app.types.models import ChoreoModel


def create_entry(entry: ChoreoModel, session: SessionDep) -> ChoreoModel:
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def get_entry_by_id(
    entry_id: UUID, Model: type[ChoreoModel], session: SessionDep
) -> ChoreoModel:
    retrieved_entry = session.get(Model, entry_id)
    if retrieved_entry == None:
        raise NoResultFound(f"{Model.__name__} Not Found with id: {entry_id}")
    return retrieved_entry


def delete_entry(entry_id: UUID, Model: type[ChoreoModel], session: SessionDep):
    try:
        entry = get_entry_by_id(entry_id, Model, session)
        session.delete(entry)
        session.commit()
    except NoResultFound as e:
        print(e)  # handle error properly at some point
