---
title: Fields
ordering: 2
---

**Fields** are used to describe separate questions inside form.

```python
from aiogram_forms.forms import Form, fields

@dispatcher.register('example')
class ExampleForm(Form):
    name = fields.TextField('Name')
    email = fields.EmailField('Email', help_text='We will send confirmation code.')
    phone = fields.PhoneNumberField('Phone number', share_contact=True)
```

## Field types

### Field
This is the base field for all fields.

<dl>
    <dt class="font-semibold">label: str</dt>
    <dd>Question label. Can be a string or <i>LazyProxy</i> from <i>aiogram.utils.i18n</i> package.</dd>
    <dt class="font-semibold">help_text: Optional[str]</dt>
    <dd>Help text displayed under the label.</dd>
    <dt class="font-semibold">error_messages: Optional[Mapping[str, str]]</dt>
    <dd>Error key to custom error message mapping. Used to overwrite default messages.</dd>
    <dt class="font-semibold">validators: List[Callable]</dt>
    <dd>List of callable objects. Used to validate user's input.</dd>
</dl>

### TextField
TextField is used for text questions and contains additional optional params to control answer length.

<dl>
    <dt class="font-semibold">min_length: Optional[int]</dt>
    <dd>Used to validate min characters in user's answer. If given <i>MinLengthValidator</i> will be added.</dd>
    <dt class="font-semibold">max_length: Optional[int]</dt>
    <dd>Used to validate max characters in user's answer. <i>MaxLengthValidator</i> will be added.</dd>
</dl>

### EmailField
Special field to ask and validate email. Adds _EmailValidator_.

### PhoneNumberField
Special field to ask and validate phone number. Adds _PhoneNumberValidator_.

<dl>
    <dt class="font-semibold">share_contact: bool = False</dt>
    <dd>If applied, will activate special keyboard, so user can send his contact with single click.</dd>
</dl>
