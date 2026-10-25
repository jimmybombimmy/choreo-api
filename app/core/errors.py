from typing import Any


def error_builder(
    Err: type[Exception],
    param: str,
    invalid_value: Any,
    correct_type: str,
) -> Exception:
    if type(invalid_value) is str:
        invalid_value = f"'{invalid_value}'"
    err_msg = f"Invalid Value: {invalid_value}, {param} must be a {correct_type}"
    return Err(err_msg)
