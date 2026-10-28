from operator import attrgetter

from app.core.config import settings

PROTOCOL, HOST, PORT, API_V1_STR = attrgetter("PROTOCOL", "HOST", "PORT", "API_V1_STR")(
    settings
)


def build_paginated_response(model_name, offset, limit, filter, order, entries):
    count = len(entries)
    base_url = f"{PROTOCOL}://{HOST}:{PORT}{API_V1_STR}/{model_name}"

    def get_next_url():
        if count < limit:
            return None
        return f"{base_url}/?limit={limit}&filter={filter}&order={order}&offset={offset + limit}"

    def get_previous_url():
        if offset == 0:
            return None

        prev_base_url = f"{base_url}?limit={limit}&filter={filter}&order={order}"
        if offset < limit:
            return f"{prev_base_url}&offset=0"
        return f"{prev_base_url}&offset={offset - limit}"

    obj = {
        "count": str(count),
        "next": get_next_url(),
        "previous": get_previous_url(),
        "offset": str(offset),
        "order": str(order),
        "filter": filter,
        "results": entries,
    }
    return obj
