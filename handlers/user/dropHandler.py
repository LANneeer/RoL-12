from aiogram.types import Message

from loader import dp, db, _


@dp.message_handler(text='999')
async def delete_in_db(message: Message):
    await db.delete_from_Teachers(message.from_user.id)
    await db.delete_from_Students(message.from_user.id)
    await message.answer(_('<b>Вы удалили вашу учетную запись</b>'))
