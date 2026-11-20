from app.api.v1.users.routes import get_all_users

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


class TestGetAllUsers:
    def test_blah(self, session_mock):
        print("hi")
