from enum import Enum


class UnaryExpressionStrings(str, Enum):
    asc = "asc"
    desc = "desc"
    nulls_first = "nulls_first"
    nulls_last = "nulls_last"
