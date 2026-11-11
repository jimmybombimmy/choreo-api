from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.api.v1.pagination import build_paginated_response
from app.db.base import SessionDep
from app.enums.query_enums import UnaryExpressionStrings
from app.models.users import User
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
- Ensure returning object also returns query information
    - √√√E.g. an entries obj inside with offset, limit, etc. after.
    - Make sure type for get_all_users is updated accordingly
- Unit tests
    - √√√build_get_all_entries_query
    - √√√execute_statement
    - build_paginated_response
    - get_all_users (make sure to use MagicMock here)
- Integration tests
    - for get_all_users
- Figure out why build_paginated_response doesn't work and fix
- √√√Find a way to make sure this returns a 200 as well
- + error codes too
- Make sure that the code is consistent and not a silly mix of OO and functional
"""


@router.get("/")
def get_all_users(
    session: SessionDep,
    offset: Offset = 0,
    limit: Limit = 50,
    filter: UserFilter = "created_at",
    order: Order = UnaryExpressionStrings.asc,
) -> JSONResponse:

    statement = build_get_all_entries_query(User, offset, limit, filter, order)

    entries = execute_statement(session, statement)

    paginated_response = build_paginated_response(
        "users", offset, limit, filter, order, entries
    )

    return JSONResponse(content=jsonable_encoder(paginated_response))
