"""
Forms and fields custom errors.
"""


class FieldValidationError(ValueError):
    """
    Field validation error.
    """
    message: str

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message
