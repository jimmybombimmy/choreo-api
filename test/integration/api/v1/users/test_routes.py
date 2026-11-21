import pytest
from operator import itemgetter

from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.users.routes import get_all_users
from app.scripts.seed.test_data import test_users
from app.core.config import settings

"""
tests
- √√√default values
- √√√offset > 0
- √√√small limit
- √√√filter by a certain thing
- √√√order desc
- √√√A bunch of different changes

sad path tests
- Basically just copy all from test/unit/services/test_services.py
- Think about their error codes
"""

build_get_all_entries_default_params = {
    "offset": 0,
    "limit": 50,
    "filter": "created_at",
    "order": "asc",
}


def sort_users_by_id(users):
    ordered_users = []

    for u in sorted(users, key=lambda item: item.id):
        ordered_users.append(u)

    return ordered_users


class TestGetAllUsers:
    def test_default_values_returns_paginated_response_when_no_params_provided(self):
        client = TestClient(app=app)

        response = client.get(url=f"{settings.API_V1_STR}/users/")
        assert response.status_code == 200

        j = response.json()
        assert j["page_size"] == len(test_users)
        assert j["total_count"] == len(test_users)
        assert j["next"] == None
        assert j["previous"] == None
        assert j["offset"] == 0
        assert j["order"] == "asc"
        assert j["sort_by"] == "created_at"

        test_users_out = []
        for user in test_users:
            test_users_out.append(user.model_dump(mode="json"))
        for x in range(len(test_users_out)):
            assert test_users_out[x]["id"] == j["results"][x]["id"]
            assert test_users_out[x]["username"] == j["results"][x]["username"]
            assert test_users_out[x]["email"] == j["results"][x]["email"]

    def test_default_values_returns_paginated_response_when_params_provided(self):
        client = TestClient(app=app)

        response = client.get(
            url=f"{settings.API_V1_STR}/users/",
            params=build_get_all_entries_default_params,
        )
        assert response.status_code == 200

        j = response.json()
        assert j["page_size"] == len(test_users)
        assert j["total_count"] == len(test_users)
        assert j["next"] == None
        assert j["previous"] == None
        assert j["offset"] == 0
        assert j["order"] == "asc"
        assert j["sort_by"] == "created_at"

        test_users_out = []
        for user in test_users:
            test_users_out.append(user.model_dump(mode="json"))
        for x in range(len(test_users_out)):
            assert test_users_out[x]["id"] == j["results"][x]["id"]
            assert test_users_out[x]["username"] == j["results"][x]["username"]
            assert test_users_out[x]["email"] == j["results"][x]["email"]

    non_default_params_cases = [
        # No HttpURL in urls due to json()
        pytest.param(
            {**build_get_all_entries_default_params, "offset": 1},
            test_users[1:3],
            {
                "next": None,
                "previous": "http://localhost:8000/api/v1/users?limit=50&filter=created_at&order=asc&offset=0",
            },
            id="offset",
        ),
        pytest.param(
            {**build_get_all_entries_default_params, "limit": 2},
            test_users[0:2],
            {
                "next": "http://localhost:8000/api/v1/users?limit=2&filter=created_at&order=asc&offset=2",
                "previous": None,
            },
            id="limit",
        ),
        pytest.param(
            {**build_get_all_entries_default_params, "limit": 1, "offset": 1},
            test_users[1:2],
            {
                "next": "http://localhost:8000/api/v1/users?limit=1&filter=created_at&order=asc&offset=2",
                "previous": "http://localhost:8000/api/v1/users?limit=1&filter=created_at&order=asc&offset=0",
            },
            id="limit+offset",
        ),
        pytest.param(
            {**build_get_all_entries_default_params, "filter": "id"},
            sort_users_by_id(test_users),
            {
                "next": None,
                "previous": None,
            },
            id="filter",
        ),
        pytest.param(
            {**build_get_all_entries_default_params, "order": "desc"},
            test_users[::-1],
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
            sort_users_by_id(sort_users_by_id(test_users)[-2:-1]),
            {
                "next": "http://localhost:8000/api/v1/users?limit=1&filter=id&order=desc&offset=2",
                "previous": "http://localhost:8000/api/v1/users?limit=1&filter=id&order=desc&offset=0",
            },
            id="all",
        ),
    ]

    @pytest.mark.parametrize("vals,results,urls", non_default_params_cases)
    def test_non_defaults(self, vals, results, urls):
        offset, limit, filter, order = itemgetter("offset", "limit", "filter", "order")(
            vals
        )
        client = TestClient(app=app)

        response = client.get(
            url=f"{settings.API_V1_STR}/users/",
            params={"offset": offset, "limit": limit, "filter": filter, "order": order},
        )
        assert response.status_code == 200

        j = response.json()
        assert j["page_size"] == len(results)
        assert j["total_count"] == len(test_users)
        assert j["next"] == urls["next"]
        assert j["previous"] == urls["previous"]
        assert j["offset"] == offset
        assert j["order"] == order
        assert j["sort_by"] == filter

        test_users_out = []
        for user in results:
            test_users_out.append(user.model_dump(mode="json"))

        for x in range(len(test_users_out)):
            assert test_users_out[x]["id"] == j["results"][x]["id"]
            assert test_users_out[x]["username"] == j["results"][x]["username"]
            assert test_users_out[x]["email"] == j["results"][x]["email"]
