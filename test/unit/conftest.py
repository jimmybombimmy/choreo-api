import pytest

from sqlmodel import Session

from app.core.db import get_session

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

    def add(self, entry):
        self.added = entry

    def commit(self):
        self.committed = True

    def refresh(self, entry):
        self.refreshed = entry

    def delete(self, entry):
        self.deleted = entry

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
