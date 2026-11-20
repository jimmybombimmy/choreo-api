from collections.abc import Sequence

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.api.v1.pagination import build_paginated_response
from app.db.base import SessionDep
from app.enums.query_enums import UnaryExpressionStrings
from app.models.users import User
from app.services.services import execute_statement
from app.services.queries import (
    build_get_all_entries_query,
    get_entries_total_count_query,
)
from app.types.schemas import ChoreoSchema
from app.types.query_params import Offset, Limit, Order, UserFilter

router = APIRouter(prefix="/users", tags=["users"])

"""
To do:
- √√√Get users by offset and limit
- Give options for filtering
    - √√√Currently it's just created_at and asc, this should be default
    - Ensure that there's proper error handling for querying an incorrect column
- √√√Ensure returning object also returns query information
    - √√√E.g. an entries obj inside with offset, limit, etc. after.
    - √√√Make sure type for get_all_users is updated accordingly
- XXXASYNC/AWAIT
    - XXXThis has been turned into a separate ticket
- Unit tests
    - √√√build_get_all_entries_query
    - √√√execute_statement
    - √√√get_entries_total_count_query
    - √√√build_paginated_response
    - get_all_users (make sure to use MagicMock here)
- Integration tests
    - get_all_users
- √√√Figure out why build_paginated_response doesn't work and fix
- √√√Find a way to make sure this returns a 200 as well
- + error codes too
- Make sure that the code is consistent and not a silly mix of OO and functional
- √√√create a function to get the total amount of values from a db
    - √√√then add that "total" to the paginated response
    - √√√Also, use this to determine whether it's right to generate a next_url
"""


@router.get("/")
def get_all_users(
    session: SessionDep,
    offset: Offset = 0,
    limit: Limit = 50,
    filter: UserFilter = "created_at",
    order: Order = UnaryExpressionStrings.asc,
) -> JSONResponse:

    get_all_statement = build_get_all_entries_query(User, offset, limit, filter, order)
    entries: Sequence[ChoreoSchema | None] = execute_statement(
        session, get_all_statement
    )

    count_statement = get_entries_total_count_query(User)
    total_count: list[int] = execute_statement(session, count_statement)

    paginated_response = build_paginated_response(
        model_name="users",
        offset=offset,
        limit=limit,
        filter=filter,
        order=order,
        total_count=total_count[0],
        entries=entries,
    )

    return JSONResponse(content=jsonable_encoder(paginated_response))
