"""
Utilities and helpers.
"""
from typing import Any, Type, Tuple


def get_attrs_of_type(obj: Any, type_: Type) -> Tuple:  # type: ignore[type-arg]
    """Get object attrs of given type."""
    return tuple(
        (key, value)
        for key, value
        in vars(obj).items()
        if isinstance(value, type_) and not key.startswith('__')
    )
