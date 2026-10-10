from uuid import UUID
from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.db.base import SessionDep
from app.types.models import ChoreoModel, ChoreoModelTypeVar
from app.types.schemas import ChoreoSchema


def execute_statement(session: SessionDep, statement) -> Sequence[ChoreoSchema]:
    entries = session.exec(statement).all()
    return entries


def create_entry(entry: ChoreoModelTypeVar, session: SessionDep) -> ChoreoModelTypeVar:
    try:
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry
    except UnmappedInstanceError:
        raise UnmappedInstanceError(
            entry, f"Incorrect data provided when creating entry: {entry}"
        )


def get_entry_by_id(
    entry_id: UUID, Model: type[ChoreoModel], session: SessionDep
) -> ChoreoModel:
    """
    Gets an entry by its ID and Model

    Errors:
    - NoResultFound - as below, if entry isn't retrieved
    - AttributeError - for issues with incorrect models
    """
    retrieved_entry = session.get(Model, entry_id)
    if retrieved_entry == None:
        raise NoResultFound(f"{Model.__name__} not found with id: {entry_id}")
    return retrieved_entry


def delete_entry(entry_id: UUID, Model: type[ChoreoModel], session: SessionDep) -> None:
    """
    Deletes an entry by its ID and Model

    Errors:
    - NoResultFound: This will be thrown if unable to find the entry when running get_entry_by_id
    """

    entry = get_entry_by_id(entry_id, Model, session)
    session.delete(entry)
    session.commit()
