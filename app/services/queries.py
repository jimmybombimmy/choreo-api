from collections.abc import Callable

from sqlalchemy import UnaryExpression
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlmodel import select

from app.types.models import ChoreoModel
from app.enums.query_enums import UnaryExpressionStrings
from app.types.query_params import Offset, Limit


# Attribute Error? https://docs.python.org/3/builtins/functions.html#getattr
def build_get_all_entries_query(
    model: type[ChoreoModel],
    offset: Offset,
    limit: Limit,
    filter: str,
    order: UnaryExpressionStrings,
):
    # These errors should never happen as long as Annotations are filtered correctly
    if offset < 0:
        raise ValueError("offset must be non-negative")
    if limit < 1:
        raise ValueError("limit must be positive")

    if filter not in model.model_fields.keys():
        raise ValueError(f"Invalid filter field: {filter}")
    filter_element: InstrumentedAttribute = getattr(model, filter)

    order_element: Callable[[], UnaryExpression] = getattr(filter_element, order)

    return select(model).order_by(order_element()).offset(offset).limit(limit)
