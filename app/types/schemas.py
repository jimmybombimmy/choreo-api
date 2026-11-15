from typing import TypeAlias, Sequence
from pydantic import BaseModel, HttpUrl

from app.schemas.user import UserOut
from app.types.query_params import Offset, Order, UserFilter
from test.unit.mocks import FakeModelOut

# to be extended as more shemas are created
ChoreoSchema: TypeAlias = UserOut | FakeModelOut  # Unit testing only


class GetAllPaginatedResponse(BaseModel):
    page_size: int
    total_count: int
    next: HttpUrl | None
    previous: HttpUrl | None
    offset: Offset
    order: Order
    sort_by: UserFilter
    results: Sequence[ChoreoSchema | None]
