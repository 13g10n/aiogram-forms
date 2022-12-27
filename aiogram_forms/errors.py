"""
Forms and fields custom errors.
"""


class ValidationError(ValueError):
    """
    Field validation error.
    """
    message: str
    code: str

    def __init__(self, message: str, code: str) -> None:
        super().__init__()
        self.message = message
        self.code = code
