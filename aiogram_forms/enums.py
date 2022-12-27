# pylint: disable=invalid-name
"""
Enums.
"""
import enum


class RouterHandlerType(enum.Enum):
    """Aiogram router handler types."""
    Update = 'update'
    Message = 'message'
    EditedMessage = 'edited_message'
    ChannelPost = 'channel_post'
    EditedChannelPost = 'edited_channel_post'
    InlineQuery = 'inline_query'
    ChosenInlineResult = 'chosen_inline_result'
    CallbackQuery = 'callback_query'
    ShippingQuery = 'shipping_query'
    PreCheckoutQuery = 'pre_checkout_query'
    Poll = 'poll'
    PollAnswer = 'poll_answer'
    Errors = 'errors'
