from operator import attrgetter
from collections.abc import Sequence
from pydantic import HttpUrl

from app.core.config import settings
from app.types.schemas import (
    GetAllPaginatedResponse,
    ChoreoSchema,
)
from app.types.query_params import Offset, Limit, Order, UserFilter
from app.utils.validate_http_url import validate_http_url

PROTOCOL, HOST, PORT, API_V1_STR = attrgetter("PROTOCOL", "HOST", "PORT", "API_V1_STR")(
    settings
)


# class PaginatedResponse:
#     def __init__(
#         self,
#         model_name: str,
#         offset: Offset,
#         limit: Limit,
#         filter: UserFilter,
#         order: Order,
#         entries: Sequence[ChoreoSchema] | Sequence[None],
#     ):
#         "count" = len(entries)
#         "next": get_next_url()
#         "previous": get_previous_url()
#         "offset": offset
#         "order": order
#         "filter": filter
#         "results": entries

#     def get_base_url(self, model_name):
#         return f"{PROTOCOL}://{HOST}:{PORT}{API_V1_STR}/{self.model_name}"

#     def get_next_url(self) -> HttpUrl | None:
#         if self.count < self.limit:
#             return None
#         return validate_http_url(
#             f"{self.base_url}/?limit={self.limit}&filter={filter}&order={self.order}&offset={self.offset + self.limit}"
#         )

#     def get_previous_url(self) -> HttpUrl | None:
#         if self.offset == 0:
#             return None

#         prev_base_url = f"{self.base_url}?limit={self.limit}&filter={filter}&order={self.order}"
#         if self.offset < self.limit:
#             return validate_http_url(f"{prev_base_url}&offset=0")
#         return validate_http_url(f"{prev_base_url}&offset={self.offset - self.limit}")


def build_paginated_response(
    model_name: str,
    offset: Offset,
    limit: Limit,
    filter: UserFilter,
    order: Order,
    entries: Sequence[ChoreoSchema | None],
) -> GetAllPaginatedResponse:
    print(f"fuck {entries}")
    count = len(entries)
    base_url = f"{PROTOCOL}://{HOST}:{PORT}{API_V1_STR}/{model_name}"

    def get_next_url() -> HttpUrl | None:
        if count < limit:
            return None
        return validate_http_url(
            f"{base_url}/?limit={limit}&filter={filter}&order={order}&offset={offset + limit}"
        )

    def get_previous_url() -> HttpUrl | None:
        if offset == 0:
            return None

        prev_base_url = f"{base_url}?limit={limit}&filter={filter}&order={order}"
        if offset < limit:
            return validate_http_url(f"{prev_base_url}&offset=0")
        return validate_http_url(f"{prev_base_url}&offset={offset - limit}")

    return GetAllPaginatedResponse(
        count=count,
        next=get_next_url(),
        previous=get_previous_url(),
        offset=offset,
        order=order,
        filter=filter,
        results=entries,
    )
