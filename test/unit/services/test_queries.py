import pytest
from operator import itemgetter

from app.services.queries import build_get_all_entries_query

from ..mocks import FakeModel

# To do
# - Create mocks

# Passing tests
# - √ All default values
# - √ offset > 0
# - √ limit > 1
# - filter by non-default
# - order by something else
# - A variety of filters

# Failing Tests
# - offset < 0
# - offset non-number
# - limit == 0
# - limit < 0
# - limit non-number
# - filter not a field in model
# - filter non-string
# - order is not a correct string
# - order is non-string
# - model isn't of type ChoreoModel


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


class TestBuildGetAllEntriesQuery:
    default_params = {"offset": 0, "limit": 50, "filter": "created_at", "order": "asc"}
    default_param_case = [pytest.param({**default_params})]

    @pytest.mark.parametrize("vals", default_param_case)
    def test_querying_by_default_values_returns_default_query(self, vals):
        offset, limit, filter, order = itemgetter("offset", "limit", "filter", "order")(
            vals
        )
        statement = build_get_all_entries_query(FakeModel, offset, limit, filter, order)

        query_arr = build_expected_query_strings(filter, order)
        for query_line in query_arr:
            assert query_line in str(statement)

        params = statement.compile().params
        assert params["param_1"] == limit
        assert params["param_2"] == offset

    non_default_params_cases = [
        pytest.param({**default_params, "offset": 5}, id="offset"),
        pytest.param({**default_params, "limit": 10}, id="limit"),
        pytest.param({**default_params, "filter": "foo"}, id="filter"),
        pytest.param({**default_params, "order": "desc"}, id="order"),
        pytest.param(
            {"offset": 20, "limit": 100, "filter": "id", "order": "desc"},
            id="all",
        ),
    ]

    @pytest.mark.parametrize("vals", non_default_params_cases)
    def test_querying_all_returns_valid_query_with_non_default_value(self, vals):
        offset, limit, filter, order = itemgetter("offset", "limit", "filter", "order")(
            vals
        )

        statement = build_get_all_entries_query(FakeModel, offset, limit, filter, order)

        query_arr = build_expected_query_strings(filter, order)
        for query_line in query_arr:
            assert query_line in str(statement)

        print(f"query_arrrr {query_arr}")

        params = statement.compile().params
        assert params["param_1"] == limit
        assert params["param_2"] == offset
