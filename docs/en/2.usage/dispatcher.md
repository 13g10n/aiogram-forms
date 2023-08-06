---
title: Dispatcher
ordering: 0
---

**Dispatcher** is the core controller of all entities processing.

Basically, you will register your forms via _dispatcher.register_ method, passing unique form name:

```python {3}
from aiogram_forms import dispatcher

@dispatcher.register('example')
class ExampleForm(Form):
    ...
```

After all attach aiogram's dispatcher to this object by calling _dispatcher.attach_ method in your setup:

```python {4}
bot = Bot(...)
dp = Dispatcher(...)

dispatcher.attach(dp)

await dp.start_polling(bot)
```
