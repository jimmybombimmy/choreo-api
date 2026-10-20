from typing import TypeAlias
from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlmodel import SQLModel, Field


class FakeModel(SQLModel, table=True):
    __tablename__ = "fake_model"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    foo: str = Field(max_length=30)
    created_at: datetime = Field(default_factory=lambda: datetime(2020, 5, 17))


test_uuid = UUID("e97943d1-b1c1-4ab6-898a-c2344a6b5b1a")

fake_entry = FakeModel(id=test_uuid, foo="bar")

MockChoreoModel: TypeAlias = FakeModel


def mock_get_entry_by_id(entry_id, _Model, _session):
    if entry_id == test_uuid:
        return fake_entry

    raise NoResultFound(f"Model not found with id: {entry_id}")


obj = object()


def blank_object_mock():
    return obj


class FakeSession:
    def __init__(self):
        self.added = None
        self.committed = False
        self.refreshed = None
        self.deleted = False
        self.got = None

    def add(self, entry):
        if entry.id != test_uuid:
            raise UnmappedInstanceError(entry, "bad entry")

        self.added = entry

    def commit(self):
        self.committed = True

    def refresh(self, entry):
        self.refreshed = entry

    def delete(self, entry):
        if entry.id != test_uuid:
            raise UnmappedInstanceError(entry, "bad entry")

        self.deleted = True

    def get(self, model, id):
        if id == test_uuid:
            return fake_entry
        return None

    def __enter__(self):
        return obj

    def __exit__(self, *args):
        pass
