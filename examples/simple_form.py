import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram_forms import Form, Field

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


class UserForm(Form):
    first_name = Field('First name')
    last_name = Field('Last name')
    email = Field('Email', validators=[lambda value: '@' in value])


@dp.message_handler(commands="start")
async def command_start(message: types.Message):
    await UserForm.start()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
