from typing import Sequence

from fastapi import APIRouter

from app.api.v1.pagination import build_paginated_response
from app.db.base import SessionDep
from app.enums.query_enums import UnaryExpressionStrings
from app.models.users import User
from app.schemas.user import UserOut
from app.services.services import execute_statement
from app.services.queries import build_get_all_entries_query
from app.types.query_params import Offset, Limit, Order, UserFilter

router = APIRouter(prefix="/users", tags=["users"])

"""
To do:
- √√√Get users by offset and limit
- Give options for filtering
    - √√√Currently it's just created_at and asc, this should be default
    - Ensure that there's proper error handling for querying an incorrect column
- √√√Ensure returning object also returns query information
    - E.g. an entries obj inside with offset, limit, etc. after.
- Unit tests
- Integration tests
"""


@router.get("/")
def get_all_users(
    session: SessionDep,
    offset: Offset = 0,
    limit: Limit = 50,
    filter: UserFilter = "created_at",
    order: Order = UnaryExpressionStrings.asc,
) -> Sequence[UserOut] | Sequence[None]:

    statement = build_get_all_entries_query(User, offset, limit, filter, order)
    entries = execute_statement(session, statement)

    return build_paginated_response(
        "users", offset, limit, filter, order.value, entries
    )
