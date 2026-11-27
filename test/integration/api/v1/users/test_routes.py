from typing import Annotated
import pytest
from unittest.mock import Mock
from operator import itemgetter, attrgetter

from fastapi import Depends
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.scripts.seed.test_data import test_users
from app.core.config import settings
from test.integration.conftest import bad_get_session
from test.utils import sort_by_id

PROTOCOL, HOST, PORT, API_V1_STR = attrgetter("PROTOCOL", "HOST", "PORT", "API_V1_STR")(
    settings
)

build_get_all_entries_default_params = {
    "offset": 0,
    "limit": 50,
    "filter": "created_at",
    "order": "asc",
}


SessionDep = Annotated[Session, Depends(bad_get_session)]


@pytest.mark.integration
class TestGetAllUsers:
    class TestExpectedPaths:
        def test_200_default_values_returns_paginated_response_when_no_params_provided(
            self,
        ):
            client = TestClient(app=app)

            response = client.get(url=f"{API_V1_STR}/users/")
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

        def test_200_default_values_returns_paginated_response_when_params_provided(
            self,
        ):
            client = TestClient(app=app)

            response = client.get(
                url=f"{API_V1_STR}/users/",
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
                    "previous": f"{PROTOCOL}://{HOST}:{PORT}/api/v1/users?limit=50&filter=created_at&order=asc&offset=0",
                },
                id="offset",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "offset": 50},
                [],
                {
                    "next": None,
                    "previous": f"{PROTOCOL}://{HOST}:{PORT}/api/v1/users?limit=50&filter=created_at&order=asc&offset=0",
                },
                id="offset>values",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "limit": 2},
                test_users[0:2],
                {
                    "next": f"{PROTOCOL}://{HOST}:{PORT}/api/v1/users?limit=2&filter=created_at&order=asc&offset=2",
                    "previous": None,
                },
                id="limit",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "limit": 1, "offset": 1},
                test_users[1:2],
                {
                    "next": f"{PROTOCOL}://{HOST}:{PORT}/api/v1/users?limit=1&filter=created_at&order=asc&offset=2",
                    "previous": f"{PROTOCOL}://{HOST}:{PORT}/api/v1/users?limit=1&filter=created_at&order=asc&offset=0",
                },
                id="limit+offset",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "filter": "id"},
                sort_by_id(test_users),
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
                sort_by_id(sort_by_id(test_users)[-2:-1]),
                {
                    "next": f"{PROTOCOL}://{HOST}:{PORT}/api/v1/users?limit=1&filter=id&order=desc&offset=2",
                    "previous": f"{PROTOCOL}://{HOST}:{PORT}/api/v1/users?limit=1&filter=id&order=desc&offset=0",
                },
                id="all",
            ),
        ]

        @pytest.mark.parametrize("vals,results,urls", non_default_params_cases)
        def test_200_non_default_values_return_paginated_response(
            self, vals, results, urls
        ):
            offset, limit, filter, order = itemgetter(
                "offset", "limit", "filter", "order"
            )(vals)
            client = TestClient(app=app)

            response = client.get(
                url=f"{API_V1_STR}/users/",
                params={
                    "offset": offset,
                    "limit": limit,
                    "filter": filter,
                    "order": order,
                },
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

        @pytest.mark.only
        def test_200_empty_db_returns_no_values_paginated_response(self, monkeypatch):

            # LEARN: execute_statement attribute is from where it's called, not where it lives (app.services.services.execute_statement)
            monkeypatch.setattr(
                "app.api.v1.users.routes.execute_statement",
                Mock(side_effect=[[], [0]]),
            )

            client = TestClient(app=app)

            response = client.get(url=f"{API_V1_STR}/users/")
            assert response.status_code == 200

            j = response.json()
            assert j["page_size"] == 0
            assert j["total_count"] == 0
            assert j["next"] == None
            assert j["previous"] == None
            assert j["offset"] == 0
            assert j["order"] == "asc"
            assert j["sort_by"] == "created_at"
            assert j["results"] == []

    # these are probably just unit tests tbf - move them?
    class TestErrorPaths:
        bad_params_cases = [
            pytest.param(
                {**build_get_all_entries_default_params, "offset": -1},
                [
                    {
                        "type": "greater_than_equal",
                        "loc": ["query", "offset"],
                        "msg": "Input should be greater than or equal to 0",
                        "input": "-1",
                        "ctx": {"ge": 0},
                    }
                ],
                id="offset<0",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "offset": "one"},
                [
                    {
                        "type": "int_parsing",
                        "loc": ["query", "offset"],
                        "msg": "Input should be a valid integer, unable to parse string as an integer",
                        "input": "one",
                    }
                ],
                id="offset=str",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "offset": True},
                [
                    {
                        "type": "int_parsing",
                        "loc": ["query", "offset"],
                        "msg": "Input should be a valid integer, unable to parse string as an integer",
                        "input": "true",
                    }
                ],
                id="offset=bool",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "limit": 0},
                [
                    {
                        "type": "greater_than_equal",
                        "loc": ["query", "limit"],
                        "msg": "Input should be greater than or equal to 1",
                        "input": "0",
                        "ctx": {"ge": 1},
                    }
                ],
                id="limit=0",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "limit": -5},
                [
                    {
                        "type": "greater_than_equal",
                        "loc": ["query", "limit"],
                        "msg": "Input should be greater than or equal to 1",
                        "input": "-5",
                        "ctx": {"ge": 1},
                    }
                ],
                id="limit<0",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "limit": False},
                [
                    {
                        "type": "int_parsing",
                        "loc": ["query", "limit"],
                        "msg": "Input should be a valid integer, unable to parse string as an integer",
                        "input": "false",
                    }
                ],
                id="limit=str/bool",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "filter": "bad_field"},
                [
                    {
                        "type": "literal_error",
                        "loc": ["query", "filter"],
                        "msg": "Input should be 'id', 'username', 'email', 'created_at' or 'updated_at'",
                        "input": "bad_field",
                        "ctx": {
                            "expected": "'id', 'username', 'email', 'created_at' or 'updated_at'",
                        },
                    }
                ],
                id="filter=invalid_str",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "filter": 123},
                [
                    {
                        "type": "literal_error",
                        "loc": ["query", "filter"],
                        "msg": "Input should be 'id', 'username', 'email', 'created_at' or 'updated_at'",
                        "input": "123",
                        "ctx": {
                            "expected": "'id', 'username', 'email', 'created_at' or 'updated_at'",
                        },
                    }
                ],
                id="filter=num",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "order": "bad_field"},
                [
                    {
                        "type": "enum",
                        "loc": ["query", "order"],
                        "msg": "Input should be 'asc', 'desc', 'distinct', 'nulls_first' or 'nulls_last'",
                        "input": "bad_field",
                        "ctx": {
                            "expected": "'asc', 'desc', 'distinct', 'nulls_first' or 'nulls_last'",
                        },
                    }
                ],
                id="filter=num",
            ),
            pytest.param(
                {**build_get_all_entries_default_params, "order": 123},
                [
                    {
                        "type": "enum",
                        "loc": ["query", "order"],
                        "msg": "Input should be 'asc', 'desc', 'distinct', 'nulls_first' or 'nulls_last'",
                        "input": "123",
                        "ctx": {
                            "expected": "'asc', 'desc', 'distinct', 'nulls_first' or 'nulls_last'",
                        },
                    }
                ],
                id="filter=num",
            ),
        ]

        @pytest.mark.parametrize("vals,detail", bad_params_cases)
        def test_422_single_incorrect_query_param_raises_error(self, vals, detail):
            offset, limit, filter, order = itemgetter(
                "offset", "limit", "filter", "order"
            )(vals)
            client = TestClient(app=app)

            response = client.get(
                url=f"{API_V1_STR}/users/",
                params={
                    "offset": offset,
                    "limit": limit,
                    "filter": filter,
                    "order": order,
                },
            )
            assert response.status_code == 422

            assert response.json()["detail"] == detail

        def test_422_multiple_incorrect_query_params_raises_error(self):
            client = TestClient(app=app)

            bad_params = {
                "offset": -1,
                "limit": "one hundred",
                "filter": "123",
                "order": "bad",
            }

            error_details = [
                {
                    "type": "greater_than_equal",
                    "loc": ["query", "offset"],
                    "msg": "Input should be greater than or equal to 0",
                    "input": "-1",
                    "ctx": {"ge": 0},
                },
                {
                    "type": "int_parsing",
                    "loc": ["query", "limit"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "one hundred",
                },
                {
                    "type": "literal_error",
                    "loc": ["query", "filter"],
                    "msg": "Input should be 'id', 'username', 'email', 'created_at' or 'updated_at'",
                    "input": "123",
                    "ctx": {
                        "expected": "'id', 'username', 'email', 'created_at' or 'updated_at'"
                    },
                },
                {
                    "type": "enum",
                    "loc": ["query", "order"],
                    "msg": "Input should be 'asc', 'desc', 'distinct', 'nulls_first' or 'nulls_last'",
                    "input": "bad",
                    "ctx": {
                        "expected": "'asc', 'desc', 'distinct', 'nulls_first' or 'nulls_last'"
                    },
                },
            ]

            response = client.get(
                url=f"{API_V1_STR}/users/",
                params=bad_params,
            )
            assert response.status_code == 422

            assert response.json()["detail"] == error_details

        def test_503_database_unavailable(self, bad_session_endpoint_fixture):
            client = TestClient(
                app=app,
            )

            response = client.get(
                url=f"{API_V1_STR}/users/",
                params={"session": bad_session_endpoint_fixture},
            )

            assert response.status_code == 503
            assert response.json()["detail"] == "Database service unavailable"
