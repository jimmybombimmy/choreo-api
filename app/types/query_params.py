from typing import Annotated, Literal
from fastapi import Query

from app.enums.query_enums import UnaryExpressionStrings

Offset = Annotated[int, Query(ge=0)]
Limit = Annotated[int, Query(ge=1, le=100)]
Order = Annotated[UnaryExpressionStrings, Query()]

UserSchemaFilterableFields = Literal[
    "id",
    "username",
    "email",
    "created_at",
    "updated_at",
]
UserFilter = Annotated[
    UserSchemaFilterableFields,
    Query(),
]
