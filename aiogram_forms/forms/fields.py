from .base import Field


class TextField(Field):
    """Simple text field."""


# class EmailField(Field):
#
#     def __init__(self, label, *args, **kwargs) -> None:
#         super().__init__(label, *args, **kwargs)
#         self.validators.append(
#             RegexValidator(
#                 EMAIL_REGEXP,
#                 error_message='Invalid email format!'
#             )
#         )
