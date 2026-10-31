from uuid import uuid4
from datetime import datetime

from sqlalchemy.exc import NoResultFound, ProgrammingError
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.services.services import (
    execute_statement,
    create_entry,
    get_entry_by_id,
    delete_entry,
)
from app.models.users import User

from ..mocks import FakeModel, test_uuid, mock_get_entry_by_id, fake_model_all_entries


class TestExecuteStatement:
    def test_correct_statement_retrieves_all_entries(self, session_mock):
        statement = """SELECT fakemodel.id, fakemodel.foo, fakemodel.created_at
        FROM fakemodels
        LIMIT :param_1 OFFSET :param_2"""

        entries = execute_statement(session_mock, statement)

        assert session_mock.execced == True
        assert entries == fake_model_all_entries

    def test_no_results_returned_if_no_results_in_db(self, session_mock):
        statement = """SELECT noresults.id, noresults.foo, noresults.created_at
        FROM noresults
        LIMIT :param_1 OFFSET :param_2"""

        entries = execute_statement(session_mock, statement)

        assert session_mock.execced == True
        assert entries == []

    def test_invalid_statement_throws_error(self, session_mock):
        statement = "cheese"

        try:
            execute_statement(session_mock, statement)
            assert False
        except SyntaxError as e:
            assert f"syntax error at or near {statement}" in str(e)
        except Exception:
            assert False

    def test_nonexistient_table_throws_error(self, session_mock):
        statement = """SELECT badtable.id, badtable.foo, badtable.created_at
        FROM badtable
        LIMIT :param_1 OFFSET :param_2"""

        try:
            execute_statement(session_mock, statement)
            assert False
        except ProgrammingError as e:
            assert f"relation does not exist" in str(e)
        except Exception:
            assert False


class TestCreateEntry:
    def test_entry_adds_and_returns_user(self, session_mock):
        entry = FakeModel(id=test_uuid, foo="bar")

        result = create_entry(entry, session_mock)

        assert result is entry
        assert session_mock.added is entry
        assert session_mock.committed
        assert session_mock.refreshed is entry

    def test_bad_entry_throws_error(self, session_mock):
        bad_entry = FakeModel(id=123, foo="bad")

        try:
            create_entry(bad_entry, session_mock)
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
        assert entry.created_at == datetime(2020, 5, 17)

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


class TestDeleteEntry:
    def test_existing_entry_deletes_user(
        self, monkeypatch, session_mock, mock_choreo_model_type
    ):
        monkeypatch.setattr(
            "app.services.services.get_entry_by_id", mock_get_entry_by_id
        )

        delete_entry(test_uuid, User, session_mock)

        assert session_mock.deleted == True
        assert session_mock.committed == True

    def test_bad_entry_throws_error_in_retrieval(
        self, monkeypatch, session_mock, mock_choreo_model_type
    ):
        monkeypatch.setattr(
            "app.services.services.get_entry_by_id", mock_get_entry_by_id
        )
        random_uuid = uuid4()

        try:
            delete_entry(random_uuid, User, session_mock)
            assert False
        except NoResultFound as e:
            assert f"Model not found with id: {random_uuid}" in str(e)
        except Exception:
            assert False

        assert session_mock.deleted == False
        assert session_mock.committed == False
