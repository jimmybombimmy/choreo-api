from uuid import uuid4

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.services.services import create_entry, get_entry_by_id
from app.models.users import User

from ..mocks import FakeModel, test_uuid


class TestCreateEntry:
    def test_entry_adds_and_returns_user(self, session_mock):
        entry = FakeModel(id=test_uuid, foo="bar")

        result = create_entry(entry, session_mock)  # ty: ignore[invalid-argument-type]

        assert result is entry
        assert session_mock.added is entry
        assert session_mock.committed
        assert session_mock.refreshed is entry

    def test_bad_entry_throws_error(self, session_mock):
        bad_entry = FakeModel(id=123, foo="bad")

        try:
            create_entry(bad_entry, session_mock)  # ty: ignore[invalid-argument-type]
            assert False
        except UnmappedInstanceError as e:
            assert "Incorrect data provided when creating entry" in str(e)
        except Exception:
            assert False


class TestGetEntryByID:
    def test_providing_id_and_model_returns_entry(
        self, session_mock, mock_choreo_model_type
    ):
        entry = get_entry_by_id(test_uuid, User, session_mock)

        assert entry.id == test_uuid
        assert entry.foo == "bar"

    def test_providing_incorrect_id_throws_error(
        self, session_mock, mock_choreo_model_type
    ):
        random_uuid = uuid4()

        try:
            get_entry_by_id(random_uuid, User, session_mock)
            assert False
        except NoResultFound as e:
            assert f"User not found with id: {random_uuid}" in str(e)
        except Exception:
            assert False

    def test_providing_bad_model_throws_error(self, session_mock):
        random_uuid = uuid4()

        mock_model = "foo"

        try:
            get_entry_by_id(random_uuid, mock_model, session_mock)
            assert False
        except AttributeError as e:
            assert "'str' object has no attribute '__name__'" in str(e)
        except Exception:
            assert False

    def test_providing_bad_model_throws_error(self, session_mock):
        random_uuid = uuid4()

        try:
            get_entry_by_id(random_uuid, "foo", session_mock)
            assert False
        except AttributeError as e:
            assert "'str' object has no attribute '__name__'" in str(e)
        except Exception:
            assert False

    def test_non_uuid_id_throws_error(self, session_mock):

        try:
            get_entry_by_id(123, User, session_mock)
            assert False
        except NoResultFound as e:
            assert f"User not found with id: 123" in str(e)
        except Exception:
            assert False
