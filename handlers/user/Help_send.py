from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp


@dp.message_handler(CommandHelp())
async def sendHelp(message: types.Message):
    await message.answer('создатель бота: @salvatttt')
