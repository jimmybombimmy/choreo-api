from sqlmodel import select, col

from app.types.models import ChoreoModel


def build_get_all_entries_query(model: type[ChoreoModel], offset: int, limit: int):
    return (
        select(model).order_by(col(model.created_at).asc()).offset(offset).limit(limit)
    )
