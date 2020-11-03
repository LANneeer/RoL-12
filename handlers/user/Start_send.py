from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from filters import Ban
from keyboards.default.Menu_buttons import back

from loader import dp, db
from state.States import TeacherRegister, StudentsRegister


# /start с диплинком (для учителей)
@dp.message_handler(CommandStart(deep_link='spc015523'), Ban())
async def sendStart_dl(message: Message):
    if not await db.exist_user(id=message.from_user.id):
        if message.from_user.username is None:
            await message.answer('<b>У вас нету имени пользователя!</b>\n'
                                 '<b>Поставьте себе имя пользователя что-бы пройти регистрацию</b>\n\n'
                                 '<u>Настройки >> Имя пользователя</u>\n'
                                 'И перейдите заново по ссылке\n\n'
                                 '<b><u>Так же НИКОГДА не меняйте ваше имя пользователя</u></b><u>, потому что оно не '
                                 'поменятся в базе данных где хранятся ваши данные! Так вы сделаете себе хуже!</u>')
        else:
            await message.answer('<b>Здравствуйте, вас приветствует ROL-bot</b>\n\n'
                                 '<u>Вас нет в базе данных учителей!</u>')
            await message.answer('Введите вашу <b><u>фамилию и имя</u></b>')
            await TeacherRegister.user_name.set()
        await message.delete()
    else:
        await message.answer('<b>Вы есть в базе данных!</b>\n'
                             'Нажите "назад":',
                             reply_markup=back)
        await message.delete()


# /start с диплинком (для учеников)
@dp.message_handler(CommandStart(deep_link='nssp12013'), Ban())
async def sendStart(message: Message):
    if not await db.exist_user(id=message.from_user.id):
        if message.from_user.username is None:
            await message.answer('<b>У вас нету имени пользователя!</b>\n'
                                 '<b>Поставьте себе имя пользователя что-бы пройти регистрацию</b>\n\n'
                                 '<u>Настройки >> Имя пользователя</u>\n'
                                 'И перейдите заново по ссылке\n\n'
                                 '<b><u>Так же НИКОГДА не меняйте ваше имя пользователя</u></b><u>, потому что оно не '
                                 'поменятся в базе данных где хранятся ваши данные! Так вы сделаете себе хуже!</u>')
        else:
            await message.answer('<b>Здравствуйте, вас приветствует ROL-bot</b>\n\n'
                                 '<u>Вас нет в базе данных учеников!</u>')
            await message.answer('Введите вашу <b><u>фамилию и имя</u></b>')
            await StudentsRegister.user_name.set()
        await message.delete()
    else:
        await message.answer('<b>Вы есть в базе данных!</b>\n'
                             'Нажмите "назад":',
                             reply_markup=back)
        await message.delete()
