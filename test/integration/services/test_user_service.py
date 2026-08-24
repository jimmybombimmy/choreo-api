from uuid import UUID

from sqlalchemy.exc import DataError, NoResultFound, ProgrammingError

from app.seed.test_data import ids
from app.services.user_service import get_user_by_id


def test_existing_user_returned(session_fixture):
    user = get_user_by_id(ids["users"][0], session_fixture)
    print(f"user retrieved: {user}")

    assert user != None


def test_non_existant_user_returned(session_fixture):
    random_uuid = UUID("b1901280-2c6a-4991-a94a-6535e37dad5d")
    try:
        get_user_by_id(random_uuid, session_fixture)
        assert False
    except NoResultFound as e:
        assert True

        if "User Not Found" not in str(e):
            assert False
    except Exception:
        assert False


def test_get_user_throws_dataerror_when_string_sent_as_id(session_fixture):
    incorrect_string_id = "steve"
    try:
        get_user_by_id(
            incorrect_string_id,  # ty: ignore[invalid-argument-type]
            session_fixture,
        )
        assert False
    except DataError as e:
        assert True

        if f'invalid input syntax for type uuid: "{incorrect_string_id}"' not in str(e):
            assert False
    except Exception:
        assert False


def test_get_user_throws_dataerror_when_number_sent_as_id(session_fixture):
    incorrect_num_id = 1234
    try:
        get_user_by_id(
            incorrect_num_id,  # ty: ignore[invalid-argument-type]
            session_fixture,
        )
        assert False
    except ProgrammingError as e:
        assert True

        if f"cannot cast type integer to uuid" not in str(e):
            assert False
    except Exception:
        assert False
