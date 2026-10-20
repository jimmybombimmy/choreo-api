from app.services.queries import build_get_all_entries_query

from ..mocks import FakeModel

# To do
# - Create mocks

# Passing tests
# - √ All default values
# - offset > 0
# - limit > 1
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


class TestBuildGetAllEntriesQuery:
    def test_querying_by_default_values_returns_default_sql(self, monkeypatch):
        offset = 0
        limit = 50
        statement = build_get_all_entries_query(
            FakeModel, offset, limit, "created_at", "asc"
        )

        expected_statement = """SELECT fake_model.id, fake_model.foo, fake_model.created_at
FROM fake_model ORDER BY fake_model.created_at ASC
 LIMIT :param_1 OFFSET :param_2"""
        assert expected_statement in str(statement)

        params = statement.compile().params
        assert params["param_1"] == limit
        assert params["param_2"] == offset
