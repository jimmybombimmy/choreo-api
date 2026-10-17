from enum import Enum


class UnaryExpressionStrings(str, Enum):
    asc = "asc"
    desc = "desc"
    disctinct = "distinct"
    nulls_first = "nulls_first"
    nulls_last = "nulls_last"
