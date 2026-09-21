from uuid import UUID
import pytest

from sqlalchemy.exc import DataError, NoResultFound, ProgrammingError, OperationalError

from app.seed.test_data import ids
from app.services.services import create_entry, get_entry_by_id
from app.models.users import User
from app.models.collections import Collection

# These tests may need to be improved by creating and tearing down User creation
# Currently they rely on the db being seeded
# You could just seed the db though???


class Test_Create_Entry:
    def test_created_entry_returned_what_was_put_in(
        self, session_fixture, collection_for_creation_fixture
    ):
        created_entry = create_entry(collection_for_creation_fixture, session_fixture)
        assert created_entry == collection_for_creation_fixture

        created_entry_id = created_entry.id

        retrieved_entry = get_entry_by_id(created_entry_id, Collection, session_fixture)
        assert created_entry == retrieved_entry

    def test_operation_error_thrown_if_connection_refused(
        self, bad_session_fixture, collection_for_creation_fixture
    ):
        try:
            create_entry(collection_for_creation_fixture, bad_session_fixture)
        except OperationalError as e:
            assert "password authentication failed for user" in str(e)
        except Exception:
            assert False

    # # maybe the same as the above??
    # def test_error_if_postgres_details_incorrect(self):
    #     assert True

    # Check if other postgres session details being incorrect will throw different errors


@pytest.mark.skip()
class Test_Get_Entry_By_ID:
    def test_existing_entry_returned(self, session_fixture):
        user = get_entry_by_id(ids["users"][0], User, session_fixture)
        print(f"user retrieved: {user}")

        assert user != None

    def test_non_existant_entry_returned(self, session_fixture):
        random_uuid = UUID("b1901280-2c6a-4991-a94a-6535e37dad5d")
        try:
            get_entry_by_id(random_uuid, User, session_fixture)
            assert False
        except NoResultFound as e:
            assert True

            if "User Not Found" not in str(e):
                assert False
        except Exception:
            assert False

    def test_get_entry_by_id_throws_dataerror_when_string_sent_as_id(
        self, session_fixture
    ):
        incorrect_string_id = "steve"
        try:
            get_entry_by_id(
                incorrect_string_id,  # ty: ignore[invalid-argument-type]
                User,
                session_fixture,
            )
            assert False
        except DataError as e:
            assert True

            if (
                f'invalid input syntax for type uuid: "{incorrect_string_id}"'
                not in str(e)
            ):
                assert False
        except Exception:
            assert False

    def test_get_user_throws_dataerror_when_number_sent_as_id(self, session_fixture):
        incorrect_num_id = 1234
        try:
            get_entry_by_id(
                incorrect_num_id,  # ty: ignore[invalid-argument-type]
                User,
                session_fixture,
            )
            assert False
        except ProgrammingError as e:
            assert True

            if f"cannot cast type integer to uuid" not in str(e):
                assert False
        except Exception:
            assert False
