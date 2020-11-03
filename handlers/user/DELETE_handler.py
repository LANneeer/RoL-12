from aiogram.types import Message

from loader import dp, db


@dp.message_handler(text='УдАлитьыь')
async def delete_in_db(message: Message):
    await db.delete_from_Teachers(message.from_user.id)
    await db.delete_from_Students(message.from_user.id)
    await message.answer('<b>вы удалены из бд</b>')
