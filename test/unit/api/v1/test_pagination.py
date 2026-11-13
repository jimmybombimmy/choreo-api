from operator import itemgetter

from app.api.v1.pagination import build_paginated_response
from test.unit.mocks import (
    fake_model_all_entries,
    fake_model_out_all_entries,
)


class TestBuildPaginatedResponse:
    pagination_default_params = {
        "model_name": "fake_model",
        "offset": 0,
        "limit": 50,
        "filter": "created_at",
        "order": "asc",
    }

    def test_default_values_entries_less_than_limit_returns_obj_with_no_next_or_previous(
        self,
    ):
        model_name, offset, limit, filter, order = itemgetter(
            "model_name", "offset", "limit", "filter", "order"
        )(self.pagination_default_params)

        result = build_paginated_response(
            model_name,
            offset,
            limit,
            filter,
            order,
            fake_model_all_entries,
        )

        assert result.count == len(fake_model_all_entries)
        assert result.next == None
        assert result.previous == None
        assert result.offset == offset
        assert result.order == order
        assert result.filter == filter
        assert result.results == fake_model_out_all_entries
