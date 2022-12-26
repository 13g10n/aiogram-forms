from typing import Optional

from ..base import Field


# class TextField(Field):
#
#     def __init__(self, label: str, *args, **kwargs) -> None:
#         super().__init__(label, *args, **kwargs)


# class BooleanField(Field):
#     # returns True/False, allow 2 (3 if with None) options
#     pass
#
#
# class ChoiceField(Field):
#     # choices
#     pass
#
#
# class NumberField(Field):
#     # max_value, min_value, decimal_places, max_digits, step_size
#     pass
#
#
# class EmailField(TextField):
#     pass
#
#
# class RegexField(TextField):
#     # regex
#     pass
#
#
# class URLField(TextField):
#     pass
#
#
# # TODO: end new fields
#
#
# class SelectField(Field):
#     _choices: List[str]
#
#     def __init__(
#             self,
#             label: str,
#             choices: List[str],
#             validators: Optional[List[Validator]] = None
#     ) -> None:
#         super().__init__(label, validators=(validators or []) + [ChoicesValidator(choices)])
#         self._choices = choices
#
#     @property
#     def reply_keyboard(self):
#         return types.ReplyKeyboardMarkup(
#             keyboard=[
#                 [
#                     types.KeyboardButton(text=choice)
#                 ] for choice in self._choices
#             ],
#             resize_keyboard=True
#         )
#
#
# class EmailField(Field):
#
#     def __init__(self, label, *args, **kwargs) -> None:
#         super().__init__(label, *args, **kwargs)
#         self._validators.append(
#             RegexValidator(
#                 EMAIL_REGEXP,
#                 error_message='Invalid email format!'
#             )
#         )
#
#
# class PhoneNumberField(Field):
#
#     def __init__(self, label, *args, **kwargs) -> None:
#         super().__init__(label, *args, **kwargs)
#         self._validators.append(
#             RegexValidator(
#                 PHONE_NUMBER_REGEXP,
#                 error_message='Invalid phone format!'
#             )
#         )
#
#     @property
#     def reply_keyboard(self):
#         return types.ReplyKeyboardMarkup(
#             keyboard=[[
#                 types.KeyboardButton(text='Share contact', request_contact=True)
#             ]],
#             resize_keyboard=True
#         )
