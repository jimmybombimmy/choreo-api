import pytest
from operator import itemgetter
from pydantic import HttpUrl

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

    non_default_params_cases = [
        pytest.param(
            {**pagination_default_params, "offset": 1},
            fake_model_out_all_entries[1:3],
            {
                "next": None,
                "previous": HttpUrl(
                    "http://localhost:8000/api/v1/fake_model?limit=50&filter=created_at&order=asc&offset=0"
                ),
            },
            id="offset",
        ),
        pytest.param(
            {**pagination_default_params, "limit": 2},
            fake_model_out_all_entries[0:2],
            {
                "next": HttpUrl(
                    "http://localhost:8000/api/v1/fake_model?limit=2&filter=created_at&order=asc&offset=2"
                ),
                "previous": None,
            },
            id="limit",
        ),
        pytest.param(
            {**pagination_default_params, "limit": 1, "offset": 1},
            fake_model_out_all_entries[1:2],
            {
                "next": HttpUrl(
                    "http://localhost:8000/api/v1/fake_model?limit=1&filter=created_at&order=asc&offset=2"
                ),
                "previous": HttpUrl(
                    "http://localhost:8000/api/v1/fake_model?limit=1&filter=created_at&order=asc&offset=0"
                ),
            },
            id="limit+offset",
        ),
    ]

    @pytest.mark.parametrize("vals,results,urls", non_default_params_cases)
    def test_changing_non_default_values_returns_valid_query(self, vals, results, urls):
        model_name, offset, limit, filter, order = itemgetter(
            "model_name", "offset", "limit", "filter", "order"
        )(vals)

        result = build_paginated_response(
            model_name,
            offset,
            limit,
            filter,
            order,
            fake_model_all_entries,
        )

        assert result.count == len(results)
        assert result.next == urls["next"]
        assert result.previous == urls["previous"]
        assert result.offset == offset
        assert result.order == order
        assert result.filter == filter
        assert result.results == results
