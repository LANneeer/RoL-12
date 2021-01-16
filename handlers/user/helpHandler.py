from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp, _


@dp.message_handler(CommandHelp())
async def help_command(message: types.Message):
    await message.answer(_('Писать ему: @salvatttt'))
