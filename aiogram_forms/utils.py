from typing import Any, Type, Tuple


def get_attrs_of_type(obj: Any, type_: Type) -> Tuple:
    return tuple(
        (key, value)
        for key, value
        in vars(obj).items()
        if isinstance(value, type_)
    )
