import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram_forms import forms, fields

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


class UserForm(forms.Form):
    name = fields.StringField('Name')
    city = fields.StringField('City', choices=(
        ('Minsk', 'minsk'),
        ('Grodno', 'grodno')
    ))
    email = fields.EmailField('Email')


@dp.message_handler(commands="start")
async def command_start(message: types.Message):
    await UserForm.start(callback=_show_info)


@dp.message_handler(commands="info")
async def command_info(message: types.Message):
    await _show_info()


async def _show_info():
    data = await UserForm.get_data()
    await bot.send_message(
        chat_id=types.Chat.get_current().id,
        text='\n'.join([
            f'{field.label}: {data[field.data_key]}'
            for field in UserForm._fields
        ])
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
