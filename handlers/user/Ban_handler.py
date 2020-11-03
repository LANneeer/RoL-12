from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from filters import Teacher
from keyboards.default import Teachers_buttons
from keyboards.default.Menu_buttons import back, yes_or_no
from loader import dp, db


@dp.message_handler(Command('ban'), Teacher())
async def banned(message: Message, state: FSMContext):
    await message.answer('<b>Вы вошли в фунцию для блокировки аккаунта пользователя!</b>')
    await message.answer('Введите аккаунт(@имя_аккаунта) пользователя, которого вы хотите заблокировать:',
                         reply_markup=back)
    await state.set_state('username_for_ban')


@dp.message_handler(state='username_for_ban')
async def write_username(message: Message, state: FSMContext):
    message.text = message.text.replace('@', '')
    if message.text.upper() == 'НАЗАД' or message.text.upper() == '🔙НАЗАД':
        await state.finish()
        await message.answer(text='<b>Главное меню</b>\n'
                                  'выберите действие с кнопок ниже\n\n'
                                  'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if len(message.text) < 34:
            id = await db.exists_with_username(message.text)
            if id is None:
                await message.answer('Такого ученика нету или он уже находиться в бан-листе!', reply_markup=back)
                await state.finish()
            else:
                await state.update_data(username=message.text)
                await state.update_data(id=id)
                await state.set_state('accept_for_ban')
                await message.answer('Хотите ли вы заблокировать этого пользователя?', reply_markup=yes_or_no)
        else:
            await message.answer('Такого аккаунта не существует, введите аккаунт повторно!', reply_markup=back)


@dp.message_handler(state='accept_for_ban')
async def accept(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data.get('id')
    username = data.get('username')
    if message.text.upper() == 'ДА':
        await db.add_ban(id=id, username=username)
        await db.del_ban(id=id)
        await state.finish()
        await message.answer('<b>Пользователь успешно заблокирован!</b>\n'
                             'Если вы хотите его разблокировать напишите "/unban"', reply_markup=Teachers_buttons)
    else:
        await message.answer('<b>Вы решили отклонить блокировку пользователя!</b>')
        await state.finish()
        await message.answer(text='<b>Главное меню</b>\n'
                                  'выберите действие с кнопок ниже\n\n'
                                  'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)


# UNBAN

@dp.message_handler(Command('unban'), Teacher())
async def banned(message: Message, state: FSMContext):
    await message.answer('<b>вы вошли в фунцию для разблокировки аккаунта пользователя!</b>')
    await message.answer('Введите аккаунт(@имя_аккаунта) пользователя, которого вы хотите разблокировать!',
                         reply_markup=back)
    await state.set_state('username_for_unban')


@dp.message_handler(state='username_for_unban')
async def write_username(message: Message, state: FSMContext):
    message.text = str(message.text).replace('@', '')
    if message.text.upper() == 'НАЗАД' or message.text.upper() == '🔙НАЗАД':
        await state.finish()
        await message.answer(text='<b>Главное меню</b>\n'
                                  'выберите действие с кнопок ниже\n\n'
                                  'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if len(message.text) < 34:
            id = await db.exists_with_username_in_ban(message.text)
            if id is None:
                await message.answer('Такого ученика нету в бан-листе, он либо разблокирован, либо не зарегистрирован!',
                                     reply_markup=back)
                await state.finish()
            else:
                await db.unban(id=id)
                await state.finish()
                await message.answer('<b>Пользователь успешно разблокирован!</b>', reply_markup=Teachers_buttons)
        else:
            await message.answer('Такого аккаунта не существует, введите повторно', reply_markup=back)
