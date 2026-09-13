from sqlmodel import Session

from app.core.db import get_session


def test_get_session_yields_session(monkeypatch):
    expected_session = object()

    class FakeSession:
        def __enter__(self):
            return expected_session

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(Session, "__enter__", FakeSession.__enter__)
    monkeypatch.setattr(Session, "__exit__", FakeSession.__exit__)

    session = next(get_session())

    assert session is expected_session
