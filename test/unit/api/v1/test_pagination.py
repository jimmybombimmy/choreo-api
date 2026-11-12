from datetime import datetime
from operator import itemgetter
from uuid import UUID

from app.api.v1.pagination import build_paginated_response
from test.unit.mocks import FakeModel, FakeModelOut


class TestBuildPaginatedResponse:
    # Make these DRY
    mock_entry_values = [
        FakeModel(
            id=UUID("852eac54-4d78-4f97-b311-6218d9ad1210"),
            foo="bar",
            created_at=datetime(2026, 10, 31, 8, 13, 59, 637574),
        ),
        FakeModel(
            id=UUID("a29526fd-998e-4c06-ac81-4702250e4c50"),
            foo="bar",
            created_at=datetime(2026, 10, 31, 8, 13, 59, 637619),
        ),
        FakeModel(
            id=UUID("620f33ab-afbe-4f06-b318-4032c1e79801"),
            foo="bar",
            created_at=datetime(2026, 10, 31, 8, 13, 59, 637638),
        ),
    ]

    mock_entry_out_values = [
        FakeModelOut(
            id=UUID("852eac54-4d78-4f97-b311-6218d9ad1210"),
            foo="bar",
            created_at=datetime(2026, 10, 31, 8, 13, 59, 637574),
        ),
        FakeModelOut(
            id=UUID("a29526fd-998e-4c06-ac81-4702250e4c50"),
            foo="bar",
            created_at=datetime(2026, 10, 31, 8, 13, 59, 637619),
        ),
        FakeModelOut(
            id=UUID("620f33ab-afbe-4f06-b318-4032c1e79801"),
            foo="bar",
            created_at=datetime(2026, 10, 31, 8, 13, 59, 637638),
        ),
    ]

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
            self.mock_entry_values,
        )

        print(f"ento {result.results}")
        print(f"unto {self.mock_entry_values}")

        assert result.count == len(self.mock_entry_values)
        assert result.next == None
        assert result.previous == None
        assert result.offset == offset
        assert result.order == order
        assert result.filter == filter
        assert result.results == self.mock_entry_out_values
