---
title: Manager
ordering: 3
---

**FormsManager** is used to start form processing and obtain form data. Instance with request data 
automatically injected in event context, so you can show any form by name from any place:

```python {1, 4-5}
from aiogram_forms.forms import FormsManager

@router.message(Command(commands=['start']))
async def command_start(message: Message, forms: FormsManager) -> None:
    await forms.show('example')
```

To fetch form data from store, you can use 
```python {3, 8}
@dispatcher.register('test-form')
class ExampleForm(Form):
    name = fields.TextField('Name')
    ...

    @classmethod
    async def callback(cls, message: types.Message, forms: FormsManager, **data) -> None:
        data = await forms.get_data(ExampleForm)
        await message.answer(text=f'Thank you, {data["name"]}!')
```
