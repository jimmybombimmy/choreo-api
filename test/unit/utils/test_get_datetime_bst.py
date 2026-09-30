from datetime import datetime
from zoneinfo import ZoneInfo

from app.utils.get_datetime_bst import get_datetime_bst


class TestGetDatetimeBST:
    def test_returns_datetime(self):
        result = get_datetime_bst()

        assert isinstance(result, datetime)

    def test_returns_europe_london_timezone(self):
        result = get_datetime_bst()

        assert result.tzinfo == ZoneInfo("Europe/London")
