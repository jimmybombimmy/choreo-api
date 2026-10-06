import pytest
from uuid import uuid4

from pydantic import PostgresDsn

from sqlalchemy import create_engine
from sqlmodel import Session

from app.core.config import settings
from app.db.base import get_session
from app.models.collections import Collection
from app.services.services import create_entry, delete_entry
from app.scripts.seed.test_data import ids, test_tasks


@pytest.fixture
def session_fixture():
    yield from get_session()


bad_engine = create_engine(
    str(
        PostgresDsn.build(
            scheme="postgresql",
            username="bad_user",
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            path=settings.POSTGRES_DB,
        )
    )
)


def bad_get_session():
    with Session(bad_engine) as session:
        yield session


@pytest.fixture
def bad_session_fixture():
    yield from bad_get_session()


@pytest.fixture
def entry_for_creation_fixture(session_fixture):
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
        print("entry_for_creation_fixture was unable to delete entry after test")


@pytest.fixture
def entry_id_for_deletion_fixture(session_fixture):
    task_id = ids["tasks"][0]
    test_task = test_tasks[0]

    yield task_id
    try:
        create_entry(test_task, session_fixture)
    except:
        print("entry_for_deletion_fixture unable to recreate entry after test")
