import pytest
from uuid import uuid4

from app.core.db import get_session
from app.models.collections import Collection
from app.services.services import delete_entry


@pytest.fixture
def session_fixture():
    yield from get_session()


@pytest.fixture
def collection_for_creation_fixture(session_fixture):
    random_uuid = uuid4()
    test_collection = Collection(
        id=random_uuid,
        name="test",
        description="test",
    )

    yield test_collection
    try:
        delete_entry(random_uuid, Collection, session_fixture)
    except:
        print("collection_fixture was unable to delete entry")
