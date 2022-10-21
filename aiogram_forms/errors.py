"""
Forms and fields custom errors.
"""
from typing import Union

from babel.support import LazyProxy


class FieldValidationError(ValueError):
    """
    Field validation error.
    """
    message: Union[str, LazyProxy]

    def __init__(self, message: Union[str, LazyProxy]) -> None:
        super().__init__()
        self.message = message
