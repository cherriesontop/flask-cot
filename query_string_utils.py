from flask import request


def int_range(
    param_name,
    default=None,
    min=None,
    max=None
        ):
    if param_name not in request.args:
        return default
    value = request.args[param_name]
    if not value:
        return default
    try:
        int_val = int(value)
    except ValueError:
        return default

    if min is not None:
        if int_val < min:
            return min

    if max is not None:
        if int_val > max:
            return max

    return int_val
