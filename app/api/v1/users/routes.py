from fastapi import APIRouter

from sqlalchemy.sql import Select

from app.services.services import execute_statement
from app.services.queries import build_get_all_entries_query
from app.db.base import SessionDep
from app.models.users import User
from app.types.query_params import Offset, Limit

router = APIRouter(prefix="/users", tags=["users"])

"""
To do:
- √√√Get users by offset and limit
- Give options for filtering
    - Currently it's just created_at and asc, this should be default
    - Ensure that there's proper error handling for querying an incorrect column
- Have search queries for users
    - Later, you may need your services to account for "name" vs "username"
    - Or build select statements
- Think about the structure you want for your database
- Ensure returning object also returns query information
    - E.g. an entries obj inside with offset, limit, etc. after.
- Unit tests
- Integration tests
"""


@router.get("/")
def get_all_users(
    session: SessionDep,
    offset: Offset = 0,
    limit: Limit = 50,
):
    statement: Select = build_get_all_entries_query(User, offset, limit)
    entries = execute_statement(session, statement)
    return entries
