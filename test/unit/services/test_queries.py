import pytest
from operator import itemgetter

from app.core.errors import error_builder
from app.services.queries import build_get_all_entries_query

from ..mocks import FakeModel, UnacceptableModel


def build_expected_query_strings(filter, order):
    """
    A simple helper function to create the str value of the expected sql query as an array

    Be warned: If 'order' is any other val than 'desc' or 'asc' in UnaryExpressionStrings
    then the order of the returning SQL Query will change and break tests.
    """

    if order.upper() == "DESC":
        order = ""

    return [
        "SELECT fake_model.id, fake_model.foo, fake_model.created_at",
        f"FROM fake_model ORDER BY fake_model.{filter} {order.upper()}",
        "LIMIT :param_1 OFFSET :param_2",
    ]


build_get_all_entries_query_default_params = {
    "offset": 0,
    "limit": 50,
    "filter": "created_at",
    "order": "asc",
}


class TestBuildGetAllEntriesQuery:
    class TestExpectedPaths:
        def test_querying_by_default_values_returns_default_query(self):
            offset, limit, filter, order = itemgetter(
                "offset", "limit", "filter", "order"
            )(build_get_all_entries_query_default_params)

            statement = build_get_all_entries_query(
                FakeModel, offset, limit, filter, order
            )

            query_arr = build_expected_query_strings(filter, order)
            for query_line in query_arr:
                assert query_line in str(statement)

            params = statement.compile().params
            assert params["param_1"] == limit
            assert params["param_2"] == offset

        non_default_params_cases = [
            pytest.param(
                {**build_get_all_entries_query_default_params, "offset": 5}, id="offset"
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "limit": 10}, id="limit"
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "filter": "foo"},
                id="filter",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "order": "desc"},
                id="order",
            ),
            pytest.param(
                {"offset": 20, "limit": 100, "filter": "id", "order": "desc"},
                id="all",
            ),
        ]

        @pytest.mark.parametrize("vals", non_default_params_cases)
        def test_querying_by_non_default_values_returns_valid_query(self, vals):
            offset, limit, filter, order = itemgetter(
                "offset", "limit", "filter", "order"
            )(vals)

            statement = build_get_all_entries_query(
                FakeModel, offset, limit, filter, order
            )

            query_arr = build_expected_query_strings(filter, order)
            for query_line in query_arr:
                assert query_line in str(statement)

            params = statement.compile().params
            assert params["param_1"] == limit
            assert params["param_2"] == offset

    class TestErrorPaths:
        error_params_cases = [
            pytest.param(
                {**build_get_all_entries_query_default_params, "offset": -1},
                ValueError,
                error_builder(ValueError, "offset", -1, "non-negative integer"),
                id="offset < 0",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "offset": "one"},
                TypeError,
                error_builder(TypeError, "offset", "one", "non-negative integer"),
                id="offset == str",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "offset": True},
                TypeError,
                error_builder(TypeError, "offset", True, "non-negative integer"),
                id="offset == bool",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "limit": 0},
                ValueError,
                error_builder(ValueError, "limit", 0, "positive integer"),
                id="limit == 0",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "limit": -5},
                ValueError,
                error_builder(ValueError, "limit", -5, "positive integer"),
                id="limit == -5",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "limit": False},
                TypeError,
                error_builder(TypeError, "limit", False, "positive integer"),
                id="limit == bool",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "filter": "bad_field"},
                ValueError,
                error_builder(
                    ValueError,
                    "filter",
                    "bad_field",
                    f"valid attribute of {FakeModel.__name__}",
                ),
                id="filter not in model",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "filter": 123},
                ValueError,
                error_builder(
                    ValueError,
                    "filter",
                    123,
                    f"valid attribute of {FakeModel.__name__}",
                ),
                id="filter == num",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "filter": False},
                ValueError,
                error_builder(
                    ValueError,
                    "filter",
                    False,
                    f"valid attribute of {FakeModel.__name__}",
                ),
                id="filter == bool",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "order": "bad_field"},
                AttributeError,
                "Neither 'InstrumentedAttribute' object nor 'Comparator' object associated with FakeModel.created_at has an attribute 'bad_field'",
                id="order not in UnaryExpressionStrings",
            ),
            pytest.param(
                {**build_get_all_entries_query_default_params, "order": 123},
                TypeError,
                error_builder(
                    TypeError,
                    "order",
                    123,
                    "valid ordering string. Accepted values: 'asc', 'desc', 'disctinct', 'nulls_first', 'nulls_last'",
                ),
                id="order != str",
            ),
        ]

        @pytest.mark.parametrize("vals,Err,err_expected", error_params_cases)
        def test_bad_args_raises_error(self, vals, Err, err_expected):
            offset, limit, filter, order = itemgetter(
                "offset", "limit", "filter", "order"
            )(vals)

            try:
                build_get_all_entries_query(FakeModel, offset, limit, filter, order)
                assert False, "Bad value did not throw error"

            except Err as e:
                assert str(err_expected) in str(e)

            except Exception as e:
                assert False, f"Incorrect exception raised {e}"

        def test_unaccepted_model_raises_error(self):

            offset, limit, filter, order = itemgetter(
                "offset", "limit", "filter", "order"
            )(build_get_all_entries_query_default_params)

            try:
                build_get_all_entries_query(
                    UnacceptableModel, offset, limit, filter, order
                )
                assert False, ""

            except TypeError as e:
                assert "model must be a ChoreoModel class" in str(e)

            except Exception as e:
                assert False, f"Incorrect exception raised {e}"

        missing_params_cases = [
            pytest.param(
                {**build_get_all_entries_query_default_params},
                "build_get_all_entries_query() missing 1 required positional argument: 'model'",
                id="no 'model'",
            ),
            pytest.param(
                {
                    "model": FakeModel,
                    "limit": 50,
                    "filter": "created_at",
                    "order": "asc",
                },
                "build_get_all_entries_query() missing 1 required positional argument: 'offset'",
                id="no 'offset'",
            ),
            pytest.param(
                {
                    "model": FakeModel,
                    "offset": 0,
                    "filter": "created_at",
                    "order": "asc",
                },
                "build_get_all_entries_query() missing 1 required positional argument: 'limit'",
                id="no 'limit'",
            ),
            pytest.param(
                {
                    "model": FakeModel,
                    "offset": 0,
                    "limit": 50,
                    "order": "asc",
                },
                "build_get_all_entries_query() missing 1 required positional argument: 'filter'",
                id="no 'filter'",
            ),
            pytest.param(
                {
                    "model": FakeModel,
                    "offset": 0,
                    "limit": 50,
                    "filter": "created_at",
                },
                "build_get_all_entries_query() missing 1 required positional argument: 'order'",
                id="no 'order'",
            ),
            pytest.param(
                {
                    "model": FakeModel,
                    "offset": 0,
                    "limit": 50,
                },
                "build_get_all_entries_query() missing 2 required positional arguments: 'filter' and 'order'",
                id="multiple missing params",
            ),
            pytest.param(
                {},
                "build_get_all_entries_query() missing 5 required positional arguments: 'model', 'offset', 'limit', 'filter', and 'order'",
                id="no params",
            ),
        ]

        @pytest.mark.parametrize("vals,err_expected", missing_params_cases)
        def test_missing_params_raises_error(self, vals, err_expected):

            try:
                build_get_all_entries_query(**vals)
                assert False
            except TypeError as e:
                assert err_expected in str(e)
            except Exception as e:
                assert False, f"Incorrect exception raised {e}"
