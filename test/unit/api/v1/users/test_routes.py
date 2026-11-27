from unittest.mock import Mock
import pytest
from operator import itemgetter, attrgetter
import datetime
from uuid import UUID
import json

from sqlalchemy import func
from sqlmodel import select
from starlette.responses import JSONResponse

from app.core.config import settings
from app.types.schemas import GetAllPaginatedResponse
from app.models.users import User
from app.api.v1.users.routes import get_all_users
from test.utils import sort_by_id

PROTOCOL, HOST, PORT, API_V1_STR = attrgetter("PROTOCOL", "HOST", "PORT", "API_V1_STR")(
    settings
)

"""
tests
- default values
- offset > 0
- small limit
- filter by a certain thing
- order desc
- A bunch of different changes

sad path tests
- Basically just copy all from test/unit/services/test_services.py
"""

build_get_all_entries_default_params = {
    "offset": 0,
    "limit": 50,
    "filter": "created_at",
    "order": "asc",
}

users_model_return = [
    User(
        email="test1@user.com",
        username="test-user1",
        created_at=datetime.datetime(2026, 11, 26, 6, 0, 41, 151115),
        id=UUID("852eac54-4d78-4f97-b311-6218d9ad1210"),
        password="pass",
        updated_at=None,
    ),
    User(
        email="test2@user.com",
        username="test-user2",
        created_at=datetime.datetime(2026, 11, 26, 6, 0, 41, 151152),
        id=UUID("a29526fd-998e-4c06-ac81-4702250e4c50"),
        password="pass",
        updated_at=None,
    ),
    User(
        email="test3@user.com",
        username="test-user3",
        created_at=datetime.datetime(2026, 11, 26, 6, 0, 41, 151171),
        id=UUID("620f33ab-afbe-4f06-b318-4032c1e79801"),
        password="pass",
        updated_at=None,
    ),
]


class TestGetAllUsers:
    def test_default_values_returns_json_response_when_no_params_provided(
        self, monkeypatch, session_mock
    ):
        offset, limit, filter, order = itemgetter("offset", "limit", "filter", "order")(
            build_get_all_entries_default_params
        )

        monkeypatch.setattr(
            "app.api.v1.users.routes.build_get_all_entries_query",
            lambda *args, **kwargs: select(User),
        )

        monkeypatch.setattr(
            "app.api.v1.users.routes.get_entries_total_count_query",
            lambda *args, **kwargs: select(func.count()).select_from(User),
        )

        monkeypatch.setattr(
            "app.api.v1.users.routes.execute_statement",
            Mock(side_effect=[users_model_return, [3]]),
        )

        monkeypatch.setattr(
            "app.api.v1.users.routes.build_paginated_response",
            lambda *args, **kwargs: GetAllPaginatedResponse(
                page_size=3,
                total_count=3,
                next=None,
                previous=None,
                offset=offset,
                order=order,
                sort_by=filter,
                results=users_model_return,
            ),
        )

        response = get_all_users(
            session=session_mock, offset=offset, limit=limit, filter=filter, order=order
        )

        assert isinstance(response, JSONResponse)
        response_json = json.loads(response.body)

        assert response_json["page_size"] == 3
        assert response_json["total_count"] == 3
        assert response_json["next"] == None
        assert response_json["previous"] == None
        assert response_json["offset"] == 0
        assert response_json["order"] == "asc"
        assert response_json["sort_by"] == "created_at"

        test_users_out = []
        for user in users_model_return:
            test_users_out.append(user.model_dump(mode="json"))
        for x in range(len(test_users_out)):
            assert test_users_out[x]["id"] == response_json["results"][x]["id"]
            assert (
                test_users_out[x]["username"] == response_json["results"][x]["username"]
            )
            assert test_users_out[x]["email"] == response_json["results"][x]["email"]
            # Password to change
            assert (
                test_users_out[x]["created_at"]
                == response_json["results"][x]["created_at"]
            )
            assert (
                test_users_out[x]["updated_at"]
                == response_json["results"][x]["updated_at"]
            )

    non_default_params_cases = [
        # No HttpURL in urls due to json()
        pytest.param(
            {**build_get_all_entries_default_params, "offset": 1},
            users_model_return[1:3],
            {
                "next": None,
                "previous": f"{PROTOCOL}://{HOST}:{PORT}{API_V1_STR}/users?limit=50&filter=created_at&order=asc&offset=0",
            },
            id="offset",
        ),
        pytest.param(
            {**build_get_all_entries_default_params, "offset": 50},
            [],
            {
                "next": None,
                "previous": f"{PROTOCOL}://{HOST}:{PORT}{API_V1_STR}/users?limit=50&filter=created_at&order=asc&offset=0",
            },
            id="offset>values",
        ),
        pytest.param(
            {**build_get_all_entries_default_params, "limit": 2},
            users_model_return[0:2],
            {
                "next": f"{PROTOCOL}://{HOST}:{PORT}{API_V1_STR}/users?limit=2&filter=created_at&order=asc&offset=2",
                "previous": None,
            },
            id="limit",
        ),
        pytest.param(
            {**build_get_all_entries_default_params, "limit": 1, "offset": 1},
            users_model_return[1:2],
            {
                "next": f"{PROTOCOL}://{HOST}:{PORT}{API_V1_STR}/users?limit=1&filter=created_at&order=asc&offset=2",
                "previous": f"{PROTOCOL}://{HOST}:{PORT}{API_V1_STR}/users?limit=1&filter=created_at&order=asc&offset=0",
            },
            id="limit+offset",
        ),
        pytest.param(
            {**build_get_all_entries_default_params, "filter": "id"},
            sort_by_id(users_model_return),
            {
                "next": None,
                "previous": None,
            },
            id="filter",
        ),
        pytest.param(
            {**build_get_all_entries_default_params, "order": "desc"},
            users_model_return[::-1],
            {
                "next": None,
                "previous": None,
            },
            id="order",
        ),
        pytest.param(
            {
                **build_get_all_entries_default_params,
                "limit": 1,
                "offset": 1,
                "filter": "id",
                "order": "desc",
            },
            # Sorted by ID, then reversed to get the second to last user
            sort_by_id(sort_by_id(users_model_return)[-2:-1]),
            {
                "next": f"{PROTOCOL}://{HOST}:{PORT}{API_V1_STR}/users?limit=1&filter=id&order=desc&offset=2",
                "previous": f"{PROTOCOL}://{HOST}:{PORT}{API_V1_STR}/users?limit=1&filter=id&order=desc&offset=0",
            },
            id="all",
        ),
    ]

    @pytest.mark.parametrize("vals,results,urls", non_default_params_cases)
    def test_non_default_values_return_json_paginated_response(
        self, monkeypatch, vals, results, urls, session_mock
    ):
        offset, limit, filter, order = itemgetter("offset", "limit", "filter", "order")(
            vals
        )

        monkeypatch.setattr(
            "app.api.v1.users.routes.build_get_all_entries_query",
            lambda *args, **kwargs: select(User),
        )

        monkeypatch.setattr(
            "app.api.v1.users.routes.get_entries_total_count_query",
            lambda *args, **kwargs: select(func.count()).select_from(User),
        )

        monkeypatch.setattr(
            "app.api.v1.users.routes.execute_statement",
            Mock(side_effect=[results, [len(results)]]),
        )

        monkeypatch.setattr(
            "app.api.v1.users.routes.build_paginated_response",
            lambda *args, **kwargs: GetAllPaginatedResponse(
                page_size=len(results),
                total_count=3,
                next=urls["next"],
                previous=urls["previous"],
                offset=offset,
                order=order,
                sort_by=filter,
                results=users_model_return,
            ),
        )

        response = get_all_users(
            session=session_mock,
            offset=offset,
            limit=limit,
            filter=filter,
            order=order,
        )

        assert isinstance(response, JSONResponse)
        response_json = json.loads(response.body)

        assert response_json["page_size"] == len(results)
        assert response_json["total_count"] == 3
        assert response_json["next"] == urls["next"]
        assert response_json["previous"] == urls["previous"]
        assert response_json["offset"] == offset
        assert response_json["order"] == order
        assert response_json["sort_by"] == filter

        test_users_out = []
        for user in users_model_return:
            test_users_out.append(user.model_dump(mode="json"))
        for x in range(len(test_users_out)):
            assert test_users_out[x]["id"] == response_json["results"][x]["id"]
            assert (
                test_users_out[x]["username"] == response_json["results"][x]["username"]
            )
            assert test_users_out[x]["email"] == response_json["results"][x]["email"]
            # Password to change
            assert (
                test_users_out[x]["created_at"]
                == response_json["results"][x]["created_at"]
            )
            assert (
                test_users_out[x]["updated_at"]
                == response_json["results"][x]["updated_at"]
            )


# Error paths are just results of already established throws.
# Skipping as a result.
