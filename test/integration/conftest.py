import pytest

from app.core.db import get_session


@pytest.fixture
def session_fixture():
    yield from get_session()
