from datetime import datetime
from zoneinfo import ZoneInfo

from app.utils.get_datetime_uk import get_datetime_uk


class TestGetDatetimeBST:
    def test_returns_datetime(self):
        result = get_datetime_uk()

        assert isinstance(result, datetime)

    def test_returns_europe_london_timezone(self):
        result = get_datetime_uk()

        assert result.tzinfo == ZoneInfo("Europe/London")
