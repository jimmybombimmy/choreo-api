from uuid import UUID, uuid4
import pytest

from sqlalchemy.exc import DataError, NoResultFound, ProgrammingError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.scripts.seed.test_data import ids
from app.services.services import create_entry, get_entry_by_id, delete_entry
from app.models.users import User
from app.models.collections import Collection
from app.models.tasks import Task


@pytest.mark.integration
class Test_Create_Entry:
    def test_created_entry_returned_what_was_put_in(
        self, session_fixture, entry_for_creation_fixture
    ):
        created_entry: Collection = create_entry(
            entry_for_creation_fixture, session_fixture
        )
        assert created_entry == entry_for_creation_fixture

        created_entry_id = created_entry.id

        retrieved_entry = get_entry_by_id(created_entry_id, Collection, session_fixture)
        assert created_entry == retrieved_entry

    def test_entry_with_incorrect_type_throws_error(self, session_fixture):
        bad_entry = (
            Task(
                id=123,
                name="Change bed sheets",
                task_list_id=ids["task_lists"][0],
            ),
        )

        try:
            create_entry(bad_entry, session_fixture)
            assert False, "Bad entry somehow created"
        except UnmappedInstanceError as e:
            assert f"Incorrect data provided when creating entry: {bad_entry}" in str(e)
        except Exception:
            assert False, "Incorrect exception given"

    def test_entry_with_missing_required_entry_throws_error(self, session_fixture):
        random_uuid = UUID("f0779f5d-c0e2-43c2-aa01-bbea0140f879")

        bad_entry = (
            Task(
                id=random_uuid,
                name="Change bed sheets",
            ),
        )

        try:
            create_entry(bad_entry, session_fixture)
            assert False, "Bad entry somehow created"
        except UnmappedInstanceError as e:
            assert f"Incorrect data provided when creating entry: {bad_entry}" in str(e)
        except Exception:
            assert False, "Incorrect exception given"

    def test_entry_with_unknown_entry_throws_error(self, session_fixture):
        random_uuid = UUID("f0779f5d-c0e2-43c2-aa01-bbea0140f879")

        bad_entry = (
            Task(
                id=random_uuid,
                name="Change bed sheets",
                task_list_id=ids["task_lists"][0],
                foo="bar",
            ),
        )
        try:
            create_entry(bad_entry, session_fixture)
            assert False, "Bad entry somehow created"
        except UnmappedInstanceError as e:
            assert f"Incorrect data provided when creating entry: {bad_entry}" in str(e)
        except Exception:
            assert False, "Incorrect exception given"

    @pytest.mark.only
    def test_operation_error_thrown_if_connection_refused(self, bad_session_fixture):
        """
        All connection errors due to bad postgres info are "OperationalErrors"

        Any "TypeError"'s are caught when the PostgresDsn.build happens (in config)
        """

        random_uuid = uuid4()
        test_collection = Collection(
            id=random_uuid,
            name="test",
            description="test",
        )

        try:
            create_entry(test_collection, bad_session_fixture)
            assert False
        except OperationalError as e:
            assert "password authentication failed for user" in str(e)
        except Exception:
            assert False


@pytest.mark.integration
class Test_Get_Entry_By_ID:
    def test_existing_entry_returned(self, session_fixture):
        user = get_entry_by_id(ids["users"][0], User, session_fixture)

        assert user != None

    def test_non_existant_entry_returned(self, session_fixture):
        random_uuid = UUID("b1901280-2c6a-4991-a94a-6535e37dad5d")
        try:
            get_entry_by_id(random_uuid, User, session_fixture)
            assert False
        except NoResultFound as e:
            assert True
            assert "User not found" in str(e)
        except Exception:
            assert False

    def test_get_entry_by_id_throws_dataerror_when_string_sent_as_id(
        self, session_fixture
    ):
        incorrect_string_id = "steve"
        try:
            get_entry_by_id(
                incorrect_string_id,
                User,
                session_fixture,
            )
            assert False
        except DataError as e:
            assert True
            assert (
                f'invalid input syntax for type uuid: "{incorrect_string_id}"' in str(e)
            )
        except Exception:
            assert False

    def test_get_user_throws_dataerror_when_number_sent_as_id(self, session_fixture):
        incorrect_num_id = 1234
        try:
            get_entry_by_id(
                incorrect_num_id,
                User,
                session_fixture,
            )
            assert False
        except ProgrammingError as e:
            assert True
            assert f"cannot cast type integer to uuid" in str(e)
        except Exception:
            assert False


@pytest.mark.integration
class Test_Delete_Entry:
    def test_delete_existing_entry(
        self, session_fixture, entry_id_for_deletion_fixture
    ):
        delete_entry(entry_id_for_deletion_fixture, Task, session_fixture)

        try:
            get_entry_by_id(ids["tasks"][0], Task, session_fixture)
            assert False, "Incorrectly retrieved id after deletion"
        except NoResultFound as e:
            assert f"Task not found with id: {entry_id_for_deletion_fixture}" in str(e)
        except Exception:
            assert False, "Incorrect exception occurred"

    def test_delete_nonexisting_entry_throws_error(self, session_fixture):
        random_uuid = UUID("3b1a72bc-e1ba-4579-934a-1d0e07719074")

        try:
            delete_entry(random_uuid, Task, session_fixture)
            assert False, "Successfully deleted entry with incorrect id"
        except NoResultFound as e:
            assert f"Task not found with id: {random_uuid}" in str(e)
        except Exception:
            assert False, "Incorrect exception occurred"
