---
title: Forms
ordering: 1
---

**Forms** alongside with fields are the main building blocks in aiogram-forms.

You will create forms to collect user data automatically step by step. Optionally, you can 
overwrite _Form.callback_ method to control behaviour after form was successfully submitted:

```python {4, 8-9}
from aiogram_forms.forms import Form

@dispatcher.register('example')
class ExampleForm(Form):
    ...

    @classmethod
    async def callback(cls, message: types.Message, **data) -> None:
        await message.answer(text='Thank you!')
```
