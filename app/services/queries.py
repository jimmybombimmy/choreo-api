from collections.abc import Callable

from sqlalchemy import UnaryExpression
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlmodel import select

from app.core.errors import error_builder
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

    if not isinstance(model, type) or not issubclass(model, ChoreoModel):
        raise TypeError("model must be a ChoreoModel class")

    # These errors should never happen as long as Annotations are filtered correctly
    # Extract this logic into another function or OOP is
    if type(offset) is not int:
        raise error_builder(TypeError, "offset", offset, "non-negative integer")
    if type(limit) is not int:
        raise error_builder(TypeError, "limit", limit, "positive integer")

    if offset < 0:
        raise error_builder(ValueError, "offset", offset, "non-negative integer")
    if limit < 1:
        raise error_builder(ValueError, "limit", limit, "positive integer")

    if filter not in model.model_fields:
        raise error_builder(
            ValueError,
            "filter",
            filter,
            f"valid attribute of {model.__name__}",
        )

    filter_element: InstrumentedAttribute = getattr(model, filter)

    try:
        order_element: Callable[[], UnaryExpression] = getattr(filter_element, order)
    except TypeError:
        raise error_builder(
            TypeError,
            "order",
            order,
            "valid ordering string. Accepted values: 'asc', 'desc', 'disctinct', 'nulls_first', 'nulls_last'",
        )

    return select(model).order_by(order_element()).offset(offset).limit(limit)
