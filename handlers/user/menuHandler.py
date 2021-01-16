from aiogram.types import Message

from filters import Students, Teacher
from keyboards.default import Teachers_buttons, Students_buttons
from loader import dp, _


# Меню, когда пишет ученик
@dp.message_handler(lambda message: message.text and message.text.lower() in ['назад', '/menu', '🔙назад'], Students())
async def student_menu(message: Message):
    await message.answer(text=_('<b>Главное меню</b>\n'
                                'выберите действие с кнопок ниже\n\n'
                                'Доп. Информация: /help'),
                         reply_markup=Students_buttons)


# Меню, когда пишет учитель
@dp.message_handler(lambda message: message.text and message.text.lower() in ['назад', '/menu', '🔙назад'], Teacher())
async def teacher_menu(message: Message):
    await message.answer(_('<b>Главное меню</b>\n'
                           'выберите действие с кнопок ниже\n\n'
                           'Доп. Информация: /help'),
                         reply_markup=Teachers_buttons)
