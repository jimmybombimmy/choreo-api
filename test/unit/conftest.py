import pytest

from sqlmodel import Session
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.core.db import get_session

from .mocks import test_uuid, fake_entry, MockChoreoModel

obj = object()


@pytest.fixture
def blank_object_mock():
    return obj


class FakeSession:
    def __init__(self):
        self.added = None
        self.committed = False
        self.refreshed = None
        self.deleted = None
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
        self.deleted = entry

    def get(self, model, id):
        if id == test_uuid:
            return fake_entry
        return None

    def __enter__(self):
        return obj

    def __exit__(self, *args):
        pass


@pytest.fixture
def get_session_mock(monkeypatch):

    monkeypatch.setattr(Session, "add", FakeSession.add)
    monkeypatch.setattr(Session, "commit", FakeSession.commit)
    monkeypatch.setattr(Session, "refresh", FakeSession.refresh)
    monkeypatch.setattr(Session, "delete", FakeSession.delete)
    monkeypatch.setattr(Session, "__enter__", FakeSession.__enter__)
    monkeypatch.setattr(Session, "__exit__", FakeSession.__exit__)

    return get_session()


@pytest.fixture
def session_mock():
    return FakeSession()


@pytest.fixture
def mock_choreo_model_type(monkeypatch):
    monkeypatch.setattr("app.models.users.User", MockChoreoModel)
