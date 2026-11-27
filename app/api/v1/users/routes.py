from collections.abc import Sequence

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.api.v1.pagination import build_paginated_response
from app.db.base import SessionDep
from app.models.users import User
from app.services.services import execute_statement
from app.services.queries import (
    build_get_all_entries_query,
    get_entries_total_count_query,
)
from app.types.schemas import ChoreoSchema
from app.types.query_params import Offset, Limit, Order, UserFilter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_all_users(
    session: SessionDep,
    offset: Offset = 0,
    limit: Limit = 50,
    filter: UserFilter = "created_at",
    order: Order = Order.asc,  # required rather than UnaryExpressions.asc as that will cause errors as a query param
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
