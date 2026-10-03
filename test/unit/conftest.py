import pytest

from sqlmodel import Session


from app.core.db import get_session

from .mocks import (
    MockChoreoModel,
    FakeSession,
)


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
    session = FakeSession()
    return session


@pytest.fixture
def mock_choreo_model_type(monkeypatch):
    monkeypatch.setattr("app.models.users.User", MockChoreoModel)
