from typing import TypeAlias, Sequence
from pydantic import BaseModel, HttpUrl

from app.schemas.user import UserOut
from app.types.query_params import Offset, Order, UserFilter

# to be extended as more shemas are created
ChoreoSchema: TypeAlias = UserOut


class GetAllPaginatedResponse(BaseModel):
    count: int
    next: HttpUrl | None
    previous: HttpUrl | None
    offset: Offset
    order: Order
    filter: UserFilter
    results: Sequence[ChoreoSchema | None]
