from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.users.routes import get_all_users
from app.scripts.seed.test_data import test_users
from app.core.config import settings

"""
tests
- √√√default values
- offset > 0
- small limit
- filter by a certain thing
- order desc
- A bunch of different changes

sad path tests
- Basically just copy all from test/unit/services/test_services.py
- Think about their error codes
"""


# Read up on testing so you can get the client to work and be tested
class TestGetAllUsers:
    def test_default_values_returns_paginated_response(self, session_fixture):
        client = TestClient(app=app)

        results = client.get(url=f"{settings.API_V1_STR}/users/")
        assert results.status_code == 200

        j = results.json()
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
            assert test_users_out[0]["id"] == j["results"][0]["id"]
            assert test_users_out[0]["username"] == j["results"][0]["username"]
            assert test_users_out[0]["email"] == j["results"][0]["email"]
