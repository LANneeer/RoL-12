from aiogram.types import ContentType, Message
from keyboards.default.mainKeyboards import back
from filters import Ban

from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=3)
@dp.message_handler(Ban(), content_types=ContentType.ANY)
async def send_back(message: Message):
    await message.answer(_('<b>Вы ввели что-то не то!</b>\nНажмите "НАЗАД"!'), reply_markup=back)
