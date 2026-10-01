from datetime import datetime
from zoneinfo import ZoneInfo


def get_datetime_uk() -> datetime:
    return datetime.now(ZoneInfo("Europe/London"))
