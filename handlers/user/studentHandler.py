import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes
from aiogram.utils.exceptions import MessageToForwardNotFound

from filters import Students
from keyboards.default import Subject_buttons, Students_buttons
from keyboards.default.mainKeyboards import back_and_send
from keyboards.default.subjectsKeyboard import subjects_list
from loader import dp, db, bot, _
from states import StudentsState, StudentsUpdates
from utils.misc import rate_limit


# FUNC СДАТЬ ДОМАШНЕЕ ЗАДАНИЕ
@dp.message_handler(
    lambda message: message.text and message.text.upper() in [_('СДАТЬ ЗАДАНИЕ'), _('СДАТЬ ЗАДАНИЕ 📤')],
    Students())
async def send_hw(message: Message):
    await message.answer(_('Выберите нужный вам <b>предмет</b>:'), reply_markup=Subject_buttons)
    await StudentsState.send_doc.set()


@dp.message_handler(state=StudentsState.send_doc)
async def select_subject(message: Message, state: FSMContext):
    subject = str(message.text).upper()
    if subject == _('🔙НАЗАД') or subject == _('НАЗАД'):
        await state.finish()
        await message.answer(text=_('<b>Главное меню</b>\n'
                                    'выберите действие с кнопок ниже\n\n'
                                    'Доп. Информация: /help'),
                             reply_markup=Students_buttons)
    else:
        if subject in subjects_list:
            await state.update_data(subject=subject.title())
            await message.answer(_('Отправьте вашу работу в виде <b>фото или документа</b>:'),
                                 reply_markup=back_and_send)
            await StudentsState.next()
        else:
            await message.answer(_('Нету такого предмета! Введите с клавиатуры!'), reply_markup=Subject_buttons)


@rate_limit(limit=0)
@dp.message_handler(state=StudentsState.send_doc2, content_types=ContentTypes.ANY)
async def send_doc(message: Message, state: FSMContext):
    answer = str(message.text).upper()
    data = await state.get_data()
    subject = data.get('subject')
    student = await db.get_student_data(message.from_user.id)
    pargroup = student[5]
    username = student[6]
    school = student[7]
    if answer == _('СДАТЬ'):
        temp_data = None
        with open('temp.json', 'r') as file:
            try:
                temp_data = json.load(file)
            except json.decoder.JSONDecodeError:
                temp_data = dict()
        if len(temp_data) != 0:
            if await db.exist_students_work(subject=subject, id=message.from_user.id):
                await db.delete_students_work(subject=subject, id=message.from_user.id)
            works_list = temp_data[str(message.from_user.id)]
            del temp_data[str(message.from_user.id)]
            with open('temp.json', 'w') as file:
                file.write(json.dumps(temp_data))
            for work in works_list:
                await db.add_students_work(id=message.from_user.id, username=username,
                                           last_name=student[4], first_name=student[3], school=school,
                                           groups=student[2].upper(),
                                           classroom_number=int(student[0]),
                                           classroom_letter=student[1], subject=subject, file_id=work,
                                           pargroup=int(pargroup))
            await state.finish()
            await message.answer(_('Задание по предмету <b>{subject}</b>, отправлено!\n').format(subject=subject),
                                 reply_markup=Students_buttons)
        else:
            await message.answer(_('<b>Вы не отправили ни одного файла!</b>\n'
                                 'Отправьте <b>файл или фото</b>, или же нажмите <b>"НАЗАД"</b>'),
                                 reply_markup=back_and_send)
    elif answer == _('НАЗАД') or answer == _('🔙НАЗАД'):
        with open('temp.json', 'r') as file:
            try:
                temp_data = json.load(file)
            except json.decoder.JSONDecodeError:
                temp_data = dict()
            try:
                del temp_data[str(message.from_user.id)]
            except KeyError:
                pass
            with open('temp.json', 'w') as f:
                f.write(json.dumps(temp_data))
        await state.finish()
        await message.answer(_('<b>Вы отменили отправку работы!</b>'))
        await message.answer(text=_('<b>Главное меню</b>\n'
                                    'выберите действие с кнопок ниже\n\n'
                                    'Доп. Информация: /help'),
                             reply_markup=Students_buttons)
    else:
        temp_data = None
        with open('temp.json', 'r', encoding='utf-8') as file:
            try:
                temp_data = json.load(file)
            except json.decoder.JSONDecodeError:
                temp_data = dict()
        with open('temp.json', 'w') as file:
            user_id = str(message.from_user.id)
            if len(temp_data.get(user_id, [])) == 5:
                await message.answer(_('Вы уже загрузили 5 файлов, нажмите кнопку <b>"СДАТЬ"</b>:'))
            else:
                temp_data[user_id] = temp_data.get(user_id, []) + [str(message.message_id)]
            file.write(json.dumps(temp_data))


# FUNC УЗНАТЬ ДОМАШНЕЕ ЗАДАНИЕ
@dp.message_handler(
    lambda message: message.text and message.text.upper() in [_('УЗНАТЬ ЗАДАНИЕ'), _('УЗНАТЬ ЗАДАНИЕ 📥')],
    Students())
async def check_hw(message: Message):
    await message.answer(_('Выберите нужный вам <b>предмет</b>:'), reply_markup=Subject_buttons)
    await StudentsState.view_doc.set()


@dp.message_handler(state=StudentsState.view_doc)
async def view_this(message: Message, state: FSMContext):
    subject = message.text.upper()
    if subject == _('🔙НАЗАД') or subject == _('НАЗАД'):
        await state.finish()
        await message.answer(text=_('<b>Главное меню</b>\n'
                                    'выберите действие с кнопок ниже\n\n'
                                    'Доп. Информация: /help'),
                             reply_markup=Students_buttons)
    else:
        if subject in subjects_list:
            student = await db.get_student_data(message.from_user.id)
            pargroup = student[5]
            school = student[7]
            file = await db.get_teachers_work(classroom_number=int(student[0]), classroom_letter=(student[1]),
                                              subject=subject.title(), group=(student[2]),
                                              pargroup=pargroup, school=school)
            if bool(len(file)):
                temp_var = None
                for file in file:
                    if temp_var != file[1]:
                        await message.answer(_('*==============================*\n\n'
                                               'Учитель по предмету: {subject}\n'
                                               'Аккаунт: @{file}').format(file=file[2], subject=subject.title()),
                                             reply_markup=Students_buttons)
                        temp_var = file[1]
                    try:
                        await bot.forward_message(chat_id=message.from_user.id, from_chat_id=file[1],
                                                  message_id=file[0])
                    except MessageToForwardNotFound:
                        await message.answer(_('<u>пользователь удалил задание</u>'))

            else:
                await message.answer(_('Задания по предмету <b>{subject}</b> не заданы!').format(subject=subject.title()
                                                                                                 ),
                                     reply_markup=Students_buttons)
            await state.finish()
        else:
            await message.answer(_('Нету такого предмета! Введите с клавиатуры!'), reply_markup=Subject_buttons)


# FUNC ЗАДАТЬ ВОПРОС
@dp.message_handler(
    lambda message: message.text and message.text.upper() in [_('ВОПРОС К УЧИТЕЛЮ'), _('ВОПРОС К УЧИТЕЛЮ ℹ️')],
    Students())
async def question(message: Message):
    student = await db.get_student_data(message.from_user.id)
    pargroup = student[5]
    school = student[7]
    teachers_username = await db.get_teachers_account(group='%'+student[2]+'%', school=school, pargroup=pargroup)
    send = _('<b>Нажмите на <i>@</i> и начните переписку!</b>\n\n')
    for data in teachers_username:
        send += _('Учитель по предмету <b>{datas}</b>: @{data}\n').format(data=data[0], datas=data[1])
    await message.answer(text=send, reply_markup=Students_buttons)


# FUNC ОТМЕТИТЬСЯ НА УРОКЕ
@dp.message_handler(
    lambda message: message.text and message.text.upper() in [_('ОТМЕТИТЬСЯ НА УРОКЕ'), _('ОТМЕТИТЬСЯ НА УРОКЕ ❗️')],
    Students())
async def check_hw(message: Message):
    await message.answer(_('Выберите нужный вам <b>предмет</b>:'), reply_markup=Subject_buttons)
    await StudentsUpdates.change_subject.set()


@dp.message_handler(state=StudentsUpdates.change_subject)
async def view_this(message: Message, state: FSMContext):
    subject = message.text.upper()
    if subject == _('🔙НАЗАД') or subject == _('НАЗАД'):
        await state.finish()
        await message.answer(text=_('<b>Главное меню</b>\n'
                                    'выберите действие с кнопок ниже\n\n'
                                    'Доп. Информация: /help'),
                             reply_markup=Students_buttons)
    else:
        if subject in subjects_list:
            student = await db.get_student_data(message.from_user.id)
            subject = subject.title()
            subject_search = '%'+subject+'%'
            group = student[2]
            group_search = '%'+group+'%'
            pargroup = student[5]
            school = student[7]
            teachers_pargroup = await db.get_teachers_pargroup(group=group_search, pargroup=pargroup,
                                                               school=school, subject=subject_search)
            if await db.exist_open_accepts(school=school, group=student[2], classroom_number=student[0],
                                           classroom_letter=student[1], pargroup=teachers_pargroup, subject=subject,
                                           accept=True):
                accepts = await db.exist_one_students_accepts(subject=subject, id=message.from_user.id,
                                                              classroom_number=student[0], classroom_letter=student[1],
                                                              group=group_search, pargroup=teachers_pargroup)
                if accepts is not None:
                    if accepts:
                        await message.answer(_('Вы уже отмечены'), reply_markup=Students_buttons)
                    else:
                        await db.update_students_accepts(id=message.from_user.id, subject=subject, accept=True)
                        await message.answer(_('Вы успешно отметились по предмету <b>{subject}</b>').format(
                                                                                                        subject=subject
                                                                                                        ),
                                             reply_markup=Students_buttons)
                else:
                    await db.add_students_accepts(id=message.from_user.id, username=student[6],
                                                  last_name=student[4], first_name=student[3], school=school,
                                                  group=student[2], classroom_number=student[0],
                                                  classroom_letter=student[1],
                                                  pargroup=teachers_pargroup, subject=subject, accepts=True)
                    await message.answer(_('Вы успешно отметились по предмету <b>{subject}</b>').format(subject=subject)
                                         , reply_markup=Students_buttons)
                await state.finish()
            else:
                await message.answer(_('Урок по предмету <b>{subject}</b> не начался').format(subject=subject),
                                     reply_markup=Students_buttons)
                await state.finish()
        else:
            await message.answer(_('Нету такого предмета! Введите с клавиатуры!'), reply_markup=Subject_buttons)
