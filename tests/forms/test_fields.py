from unittest.mock import patch, Mock

import pytest
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from aiogram_forms.forms import fields


@patch('aiogram_forms.forms.validators.MinLengthValidator')
@patch('aiogram_forms.forms.validators.MaxLengthValidator')
def test_text_field_adds_validators(min_validator, max_validator):
    text_field = fields.TextField('Text', min_length=3, max_length=5)
    assert len(text_field.validators) == 2
    assert min_validator.called
    assert max_validator.called


@patch('aiogram_forms.forms.validators.EmailValidator')
def test_email_field_adds_validators(validator):
    text_field = fields.EmailField('Email')
    assert len(text_field.validators) == 1
    assert validator.called


@patch('aiogram_forms.forms.validators.PhoneNumberValidator')
def test_phone_field_adds_validators(validator):
    text_field = fields.PhoneNumberField('Phone')
    assert len(text_field.validators) == 1
    assert validator.called


def test_phone_field_default_reply_keyboard():
    field = fields.PhoneNumberField('Phone')
    assert isinstance(field.reply_keyboard, ReplyKeyboardRemove)


def test_phone_field_adds_reply_keyboard():
    field = fields.PhoneNumberField('Phone', share_contact=True)
    assert isinstance(field.reply_keyboard, ReplyKeyboardMarkup)


@pytest.mark.asyncio
async def test_phone_field_extract_default(message):
    field = fields.PhoneNumberField('Phone')
    value = await field.extract(message)
    assert value is message.text


@pytest.mark.asyncio
async def test_phone_field_extract_shared_contact(contact_message):
    field = fields.PhoneNumberField('Phone')
    value = await field.extract(contact_message)
    assert value is contact_message.contact.phone_number


@pytest.mark.asyncio
async def test_sync_function_validator():
    def validator(value: str):
        ...

    field = fields.Field('Test', validators=[validator])
    await field.validate('value')


@pytest.mark.asyncio
async def test_async_function_validator():
    async def validator(value: str):
        ...

    field = fields.Field('Test', validators=[validator])
    await field.validate('value')


@pytest.mark.asyncio
async def test_sync_class_validator():
    class Validator:
        def __call__(self, *args, **kwargs):
            ...

    field = fields.Field('Test', validators=[Validator()])
    await field.validate('value')


@pytest.mark.asyncio
async def test_async_class_validator():
    class Validator:
        async def __call__(self, *args, **kwargs):
            ...

    field = fields.Field('Test', validators=[Validator()])
    await field.validate('value')


@pytest.mark.asyncio
async def test_choice_field_process_exists():
    field = fields.ChoiceField('Status', choices=[
        ('Published', 1),
        ('Drafted', 0)
    ])
    value = await field.process('Published')
    assert value == 1


@pytest.mark.asyncio
async def test_choice_field_process_not_exists():
    field = fields.ChoiceField('Status', choices=[
        ('Published', 1),
        ('Drafted', 0)
    ])
    value = await field.process('Trashed')
    assert value is None


def test_choice_field_reply_keyboard():
    field = fields.ChoiceField('Status', choices=[
        ('Published', 1),
        ('Drafted', 0)
    ])
    assert isinstance(field.reply_keyboard, ReplyKeyboardMarkup)

    for option, keyboard_row in zip(field.choices, field.reply_keyboard.keyboard):
        assert option[0] == keyboard_row[0].text
