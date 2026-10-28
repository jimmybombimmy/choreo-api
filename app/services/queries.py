from collections.abc import Callable

from sqlalchemy import UnaryExpression
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlmodel import select
from sqlmodel.sql.expression import SelectOfScalar

from app.core.errors import error_builder
from app.types.models import ChoreoModel
from app.enums.query_enums import UnaryExpressionStrings
from app.types.query_params import Offset, Limit


def validate_model(model: type[ChoreoModel]) -> None:
    if not isinstance(model, type) or not issubclass(model, ChoreoModel):
        raise error_builder(TypeError, "model", model, "ChoreoModel class")


def validate_pagination(offset: Offset, limit: Limit) -> None:
    if type(offset) is not int:
        raise error_builder(TypeError, "offset", offset, "non-negative integer")
    if type(limit) is not int:
        raise error_builder(TypeError, "limit", limit, "positive integer")

    if offset < 0:
        raise error_builder(ValueError, "offset", offset, "non-negative integer")
    if limit < 1:
        raise error_builder(ValueError, "limit", limit, "positive integer")


def validate_filter(model: type[ChoreoModel], filter: str) -> None:
    if filter not in model.model_fields:
        raise error_builder(
            ValueError,
            "filter",
            filter,
            f"valid attribute of {model.__name__}",
        )


def build_get_all_entries_query(
    model: type[ChoreoModel],
    offset: Offset,
    limit: Limit,
    filter: str,
    order: UnaryExpressionStrings,
) -> SelectOfScalar:

    validate_model(model)
    validate_pagination(offset, limit)
    validate_filter(model, filter)

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
