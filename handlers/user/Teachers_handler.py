import json
from random import randint

from aiogram.utils.exceptions import MessageToForwardNotFound, TelegramAPIError
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes
from aiogram.utils.exceptions import Unauthorized

from filters import Teacher
from keyboards.default import OnePlus
from keyboards.default.Menu_buttons import classroom_number, classroom_letter, back, numbers_list, letters_list, \
    back_and_send
from keyboards.default.Teacher_menu import Teachers_buttons
from loader import dp, db, bot
from state import SendWork, GetWork, Advert, TellWork, TeachersUpdates
from utils.misc import rate_limit


# FUNC ОТПРАВИТЬ ЗАДАНИЯ

@dp.message_handler(
    lambda message: message.text and message.text.upper() in ['ОТПРАВИТЬ ЗАДАНИЯ', 'ОТПРАВИТЬ ЗАДАНИЯ 📤'],
    Teacher())
async def send_HW_TWO(message: Message, state: FSMContext):
    teacher_data = await db.get_teacher_data(message.from_user.id)
    subject = teacher_data[0]
    group = teacher_data[1]
    pargroup = teacher_data[2]
    school = teacher_data[3]
    await state.update_data(subject=subject, group=group, pargroup=pargroup, school=school)
    await message.answer('Введите <b>один из ваших предметов</b>, по которому собираетесь задать работы:',
                         reply_markup=OnePlus(
                             text=subject.split(', '),
                         ).reply_keyboard)
    await SendWork.change_subject.set()


@dp.message_handler(state=SendWork.change_subject)
async def get_subject(message: Message, state: FSMContext):
    subject = message.text.upper()
    if subject == '🔙НАЗАД' or subject == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        subjects_teacher = (await state.get_data()).get('subject')
        group_teacher = (await state.get_data()).get('group')
        if subject.title() in subjects_teacher.split(', '):
            await state.update_data(subject=subject.title())
            await message.answer('Введите <b>один из ваших отделений</b>, по которому собираетесь задать работы:',
                                 reply_markup=OnePlus(
                                     text=group_teacher.split('/'),
                                 ).reply_keyboard)
            await SendWork.next()
        else:
            await message.answer('Это <b>не ваш</b> предмет!')


@dp.message_handler(state=SendWork.change_group)
async def get_group(message: Message, state: FSMContext):
    group = message.text.upper()
    if group == '🔙НАЗАД' or group == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        group_teacher = (await state.get_data()).get('group')
        if group in group_teacher.split('/'):
            await state.update_data(group=group.upper())
            await message.answer('Выберите <b>номер</b> класса, которому собираетесь отправить задание:',
                                 reply_markup=classroom_number)
            await SendWork.next()
        else:
            await message.answer('Это <b>не ваше</b> отделение!')


@dp.message_handler(state=SendWork.classroomNumber)
async def get_number(message: Message, state: FSMContext):
    answer = message.text.upper()
    if answer == '🔙НАЗАД' or answer == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if answer in numbers_list:
            await state.update_data(classroomNumber=answer)
            await message.answer('Выберите <b>букву</b> класса', reply_markup=classroom_letter)
            await SendWork.next()
        else:
            await message.answer('Пожалуйста выберите <b>число из списка</b>:', reply_markup=classroom_number)


@dp.message_handler(state=SendWork.classroomLetter)
async def get_letter(message: Message, state: FSMContext):
    answer = message.text.upper()
    if answer == '🔙НАЗАД' or answer == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if answer in letters_list:
            await state.update_data(classroomLetter=answer)
            await message.answer('Отправьте <b>документ или фото</b> с заданием!', reply_markup=back_and_send)
            await SendWork.next()
        else:
            await message.answer('Пожалуйста выберите <b>букву из списка</b>:', reply_markup=classroom_letter)


@rate_limit(limit=0)
@dp.message_handler(state=SendWork.files_id, content_types=ContentTypes.ANY)
async def get_document(message: Message, state: FSMContext):
    answer = str(message.text).upper()
    if answer == 'СДАТЬ':
        data = await state.get_data()
        group = data.get('group')
        pargroup = data.get('pargroup')
        school = data.get('school')
        classroomNumber = data.get('classroomNumber')
        classroomLetter = data.get('classroomLetter')
        subject = data.get('subject')
        if await db.exist_teachers_work(subject=subject, group=group, pargroup=pargroup,
                                        classroom_number=int(classroomNumber),
                                        classroom_letter=classroomLetter, school=school):
            await db.delete_teachers_work(subject=subject, group=group, pargroup=pargroup,
                                          classroom_number=int(classroomNumber),
                                          classroom_letter=classroomLetter, school=school)
        temp_data = None
        with open('temp.json', 'r') as file:
            try:
                temp_data = json.load(file)
            except json.decoder.JSONDecodeError:
                temp_data = dict()
        if len(temp_data) != 0:
            works_list = temp_data[str(message.from_user.id)]
            del temp_data[str(message.from_user.id)]
            with open('temp.json', 'w') as file:
                file.write(json.dumps(temp_data))
            for file in works_list:
                await db.add_teachers_work(id=message.from_user.id, username=message.from_user.username,
                                           school=school, groups=group,
                                           classroom_number=int(classroomNumber),
                                           classroom_letter=classroomLetter,
                                           subject=subject, file_id=file, pargroup=int(pargroup))
            await state.finish()
            await message.answer(f'Задание для {classroomNumber} "{classroomLetter}" успешно отправлено!',
                                 reply_markup=Teachers_buttons)
        else:
            await message.answer('<b>Вы не отправили ни одного файла!</b>\n'
                                 'Отправьте <b>файл или фото</b>, или же нажмите <b>"НАЗАД"</b>',
                                 reply_markup=back_and_send)
    elif answer == '🔙НАЗАД' or answer == 'НАЗАД':
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
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        temp_data = None
        with open('temp.json', 'r', encoding='utf-8') as file:
            try:
                temp_data = json.load(file)
            except json.decoder.JSONDecodeError:
                temp_data = dict()
        if not isinstance(temp_data, dict):
            temp_data[message.from_user.id] = [str(message.message_id)]
        with open('temp.json', 'w') as file:
            user_id = str(message.from_user.id)
            if len(temp_data.get(user_id, [])) == 5:
                await message.answer('Вы уже загрузили 5 файлов, нажмите кнопку <b>"СДАТЬ"</b>:')
            else:
                temp_data[user_id] = temp_data.get(user_id, []) + [str(message.message_id)]
            file.write(str(json.dumps(temp_data)))


# FUNC Получить работы!

@dp.message_handler(lambda message: message.text and message.text.upper() in ['ПОЛУЧИТЬ РАБОТЫ', 'ПОЛУЧИТЬ РАБОТЫ 📥'],
                    Teacher())
async def get_works(message: Message, state: FSMContext):
    teacher_data = await db.get_teacher_data(message.from_user.id)
    subject = teacher_data[0]
    group = teacher_data[1]
    pargroup = teacher_data[2]
    school = teacher_data[3]
    await state.update_data(subject=subject, group=group, pargroup=pargroup, school=school)
    await message.answer('Введите <b>один из ваших предметов</b> по которому собираетесь получить работы:',
                         reply_markup=OnePlus(
                             text=subject.split(', '),
                         ).reply_keyboard)
    await GetWork.change_subject.set()


@dp.message_handler(state=GetWork.change_subject)
async def get_subject(message: Message, state: FSMContext):
    subject = message.text.upper()
    if subject == '🔙НАЗАД' or subject == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        subjects_teacher = (await state.get_data()).get('subject')
        group_teacher = (await state.get_data()).get('group')
        if subject.title() in subjects_teacher.split(', '):
            await state.update_data(subject=subject.title())
            await message.answer('Введите <b>один из ваших отделений</b>, по которому собираетесь получить работы:',
                                 reply_markup=OnePlus(
                                     text=group_teacher.split('/'),
                                 ).reply_keyboard)
            await GetWork.next()
        else:
            await message.answer('Это <b>не ваш</b> предмет!')


@dp.message_handler(state=GetWork.change_group)
async def get_group(message: Message, state: FSMContext):
    group = message.text.upper()
    if group == '🔙НАЗАД' or group == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        group_teacher = (await state.get_data()).get('group')
        if group in group_teacher.split('/'):
            await state.update_data(group=group.upper())
            await message.answer('Выберите <b>номер</b> класса, у которого собираетесь получить работы:',
                                 reply_markup=classroom_number)
            await GetWork.next()
        else:
            await message.answer('Это <b>не ваше</b> отделение!')


@dp.message_handler(state=GetWork.classroomNumber)
async def get_number(message: Message, state: FSMContext):
    number = message.text.upper()
    if number == '🔙НАЗАД' or number == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if number in numbers_list:
            await state.update_data(classroomNumber=number)
            await message.answer('Выберите <b>букву</b> класса', reply_markup=classroom_letter)
            await GetWork.next()
        else:
            await message.answer('Пожалуйста выберите <b>число из списка</b>:', reply_markup=classroom_number)


@dp.message_handler(state=GetWork.classroomLetter)
async def get_caption(message: Message, state: FSMContext):
    letter = str(message.text).upper()
    if letter == '🔙НАЗАД' or letter == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if letter in letters_list:
            data = await state.get_data()
            classroomNumber = data.get('classroomNumber')
            classroomLetter = letter
            subject = data.get('subject')
            group = data.get('group')
            school = data.get('school')
            pargroup = data.get('pargroup')
            if pargroup == 0:
                works = sorted(await db.get_students_work0(classroom_number=int(classroomNumber),
                                                          classroom_letter=classroomLetter,
                                                          subject=subject, group=group,
                                                          school=school), key=lambda x: x[4])
            else:
                works = sorted(await db.get_students_work(classroom_number=int(classroomNumber),
                                                          classroom_letter=classroomLetter,
                                                          subject=subject, group=group,
                                                          pargroup=pargroup, school=school), key=lambda x: x[4])
            temp_var = None
            if len(works) < 1:
                await message.answer(f'Пока что, никто не отправил задания с {classroomNumber} "{classroomLetter}"\n'
                                     '<b>Или же вы ранее получили их работы!</b>', reply_markup=Teachers_buttons)
            else:
                unic_id = randint(0, 99999)
                await message.answer(f'Уникальный идентификатор полученных работ: {unic_id}\n'
                                     f'Работы учеников {classroomNumber} "{classroomLetter}":',
                                     reply_markup=Teachers_buttons)
                for work in works:
                    if temp_var != work[4]:
                        await message.answer('*==============================*\n\n'
                                             f'Фамилия: {work[0]}\nИмя: {work[1]}\nАккаунт: @{work[3]}')
                        temp_var = work[4]
                    try:
                        await bot.forward_message(chat_id=message.from_user.id, from_chat_id=work[4],
                                                  message_id=work[2])
                    except MessageToForwardNotFound:
                        await message.answer('<u>пользователь удалил задание</u>')
                    await db.delete_students_file(id=work[4], subject=subject, file_id=work[2])
            await state.finish()
        else:
            await message.answer('Пожалуйста выберите <b>букву из списка</b>:', reply_markup=classroom_letter)


# FUNC Создать объявление!

@dp.message_handler(lambda message: message.text and message.text.upper() in ['СОЗДАТЬ ОБЪЯВЛЕНИЕ',
                                                                              'СОЗДАТЬ ОБЪЯВЛЕНИЕ ✏️'], Teacher())
async def advertise(message: Message, state: FSMContext):
    teacher_data = await db.get_teacher_data(message.from_user.id)
    subject = teacher_data[0]
    group = teacher_data[1]
    pargroup = teacher_data[2]
    school = teacher_data[3]
    await state.update_data(subject=subject, group=group, pargroup=pargroup, school=school)
    await message.answer('Введите <b>один из ваших предметов</b> по которому собираетесь создать объявление:',
                         reply_markup=OnePlus(
                             text=subject.split(', '),
                         ).reply_keyboard)
    await Advert.change_subject.set()


@dp.message_handler(state=Advert.change_subject)
async def get_subject(message: Message, state: FSMContext):
    subject = message.text.upper()
    if subject == '🔙НАЗАД' or subject == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        subjects_teacher = (await state.get_data()).get('subject')
        group_teacher = (await state.get_data()).get('group')
        if subject.title() in subjects_teacher.split(', '):
            await state.update_data(subject=subject.title())
            await message.answer('Введите <b>один из ваших отделений</b>, по которому собираетесь создать объявление:',
                                 reply_markup=OnePlus(
                                     text=group_teacher.split('/'),
                                 ).reply_keyboard)
            await Advert.next()
        else:
            await message.answer('Это <b>не ваш</b> предмет!')


@dp.message_handler(state=Advert.change_group)
async def get_group(message: Message, state: FSMContext):
    group = message.text.upper()
    if group == '🔙НАЗАД' or group == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        group_teacher = (await state.get_data()).get('group')
        if group in group_teacher.split('/'):
            await state.update_data(group=group)
            await message.answer('Выберите <b>номер</b> класса, для которого собираетесь создать объявление:',
                                 reply_markup=classroom_number)
            await Advert.next()
        else:
            await message.answer('Это <b>не ваше</b> отделение!')


@dp.message_handler(state=Advert.classroomNumber)
async def get_number(message: Message, state: FSMContext):
    number = message.text.upper()
    if number == '🔙НАЗАД' or number == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if number in numbers_list:
            await state.update_data(classroomNumber=number)
            await message.answer('Выберите <b>букву</b> класса', reply_markup=classroom_letter)
            await Advert.next()
        else:
            await message.answer('Пожалуйста выберите <b>число из списка</b>:', reply_markup=classroom_number)


@dp.message_handler(state=Advert.classroomLetter)
async def get_letter(message: Message, state: FSMContext):
    letter = message.text.upper()
    if letter == '🔙НАЗАД' or letter == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if letter in letters_list:
            await state.update_data(classroomLetter=letter)
            await message.answer('Отправьте <b>сообщение</b>, которое вы хотите поставить в известность!',
                                 reply_markup=back)
            await Advert.next()
        else:
            await message.answer('Пожалуйста выберите <b>букву из списка</b>:', reply_markup=classroom_letter)


@rate_limit(limit=0)
@dp.message_handler(state=Advert.messages, content_types=ContentTypes.ANY)
async def get_message(message: Message, state: FSMContext):
    answer = str(message.text).upper()
    if answer == '🔙НАЗАД' or answer == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        data = await state.get_data()
        classroomNumber = data.get('classroomNumber')
        classroomLetter = data.get('classroomLetter')
        subject = data.get('subject')
        school = data.get('school')
        pargroup = data.get('pargroup')
        group = data.get('group')
        ids = await db.get_students_id(classroom_number=int(classroomNumber), classroom_letter=classroomLetter,
                                       group=group, pargroup=pargroup, school=school)
        if bool(len(ids)) is False:
            ids = await db.get_students_id0(classroom_number=int(classroomNumber), classroom_letter=classroomLetter,
                                            group=group, school=school)
        if bool(len(ids)):
            for id in ids:
                try:
                    await bot.send_message(chat_id=id[0], text=f'Сообщение от учителя по предмету {subject}: ')
                    await message.forward(chat_id=id[0])
                except (Unauthorized, TelegramAPIError):
                    user = await db.find_student(id[0])
                    await message.answer(f'У пользователя {user[1]} {user[0]} из класса, бот заблокирован!')
            await message.answer(f'Объявление для {classroomNumber}{classroomLetter} успешно разослано!',
                                 reply_markup=Teachers_buttons)
        else:
            await message.answer('<b>В выбранном вами классе нету людей!</b>', reply_markup=Teachers_buttons)
        await state.finish()


# FUNC ИНФА О ЗАДАНИЯХ
@dp.message_handler(
    lambda message: message.text and message.text.upper() in ['СВЕДЕНИЯ О РАБОТАХ', 'СВЕДЕНИЯ О РАБОТАХ 📎'],
    Teacher())
async def tell_work(message: Message, state: FSMContext):
    teacher_data = await db.get_teacher_data(message.from_user.id)
    subject = teacher_data[0]
    group = teacher_data[1]
    pargroup = teacher_data[2]
    school = teacher_data[3]
    await state.update_data(subject=subject, group=group, pargroup=pargroup, school=school)
    await message.answer('Введите <b>один из ваших предметов</b>, по которому собираетесь получить сведения:',
                         reply_markup=OnePlus(
                             text=subject.split(', '),
                         ).reply_keyboard)
    await TellWork.change_subject.set()


@dp.message_handler(state=TellWork.change_subject)
async def get_subject(message: Message, state: FSMContext):
    subject = message.text.upper()
    if subject == '🔙НАЗАД' or subject == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        subjects_teacher = (await state.get_data()).get('subject')
        group_teacher = (await state.get_data()).get('group')
        if subject.title() in subjects_teacher.split(', '):
            await state.update_data(subject=subject.title())
            await message.answer('Введите <b>один из ваших отделений</b>, по которому собираетесь получить сведения:',
                                 reply_markup=OnePlus(
                                     text=group_teacher.split('/'),
                                 ).reply_keyboard)
            await TellWork.next()
        else:
            await message.answer('Это <b>не ваш</b> предмет!')


@dp.message_handler(state=TellWork.change_group)
async def get_group(message: Message, state: FSMContext):
    group = message.text.upper()
    if group == '🔙НАЗАД' or group == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        group_teacher = (await state.get_data()).get('group')
        if group in group_teacher.split('/'):
            await state.update_data(group=group.upper())
            await message.answer('Выберите <b>номер</b> класса, у которого собираетесь получить сведения:',
                                 reply_markup=classroom_number)
            await TellWork.next()
        else:
            await message.answer('Это <b>не ваше</b> отделение!')


@dp.message_handler(state=TellWork.classroomNumber)
async def get_classroomNumber(message: Message, state: FSMContext):
    number = message.text.upper()
    if number == '🔙НАЗАД' or number == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if number in numbers_list:
            await state.update_data(classroomNumber=int(number))
            await message.answer('Выберите <b>букву</b> класса', reply_markup=classroom_letter)
            await TellWork.next()
        else:
            await message.answer('Пожалуйста выберите <b>число из списка</b>:', reply_markup=classroom_number)


@dp.message_handler(state=TellWork.classroomLetter)
async def get_classroomLetter(message: Message, state: FSMContext):
    letter = message.text.upper()
    data = await state.get_data()
    subject = data.get('subject')
    group = data.get('group')
    school = data.get('school')
    pargroup = data.get('pargroup')
    classroomNumber = data.get('classroomNumber')
    if letter == '🔙НАЗАД' or letter == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if letter in letters_list:
            send = f'Сведения по предмету {subject} в {classroomNumber}"{letter}":\n'
            if pargroup == 0:
                students = await db.exist_students_for_work0(classroom_number=classroomNumber, classroom_letter=letter,
                                                             group=group, school=school)
            else:
                students = await db.exist_students_for_work1(classroom_number=classroomNumber, classroom_letter=letter,
                                                             pargroup=pargroup, group=group, school=school)
            for data in students:
                works = await db.exist_students_for_work2(id=data[2], subject=subject)
                send += f'{data[0]} {data[1]}: {"✅" * works + "❌" * (1 - works)}\n'
            await message.answer(text=send, reply_markup=Teachers_buttons)
            await state.finish()
        else:
            await message.answer('Пожалуйста выберите <b>букву из списка</b>:', reply_markup=classroom_letter)


# FUNC ИНФА ОБ УЧЕНИКАХ
@dp.message_handler(
    lambda message: message.text and message.text.upper() in ['ОТКРЫТЬ УРОК', 'ОТКРЫТЬ УРОК ⏰'],
    Teacher())
async def tell_work(message: Message, state: FSMContext):
    teacher_data = await db.get_teacher_data(message.from_user.id)
    subject = teacher_data[0]
    group = teacher_data[1]
    pargroup = teacher_data[2]
    school = teacher_data[3]
    await state.update_data(subject=subject, group=group, pargroup=pargroup, school=school)
    await message.answer('Введите <b>один из ваших предметов</b>, по которому собираетесь получить сведения:',
                         reply_markup=OnePlus(
                             text=subject.split(', '),
                         ).reply_keyboard)
    await TeachersUpdates.change_subject.set()


@dp.message_handler(state=TeachersUpdates.change_subject)
async def get_subject(message: Message, state: FSMContext):
    subject = message.text.upper()
    if subject == '🔙НАЗАД' or subject == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        subjects_teacher = (await state.get_data()).get('subject')
        group_teacher = (await state.get_data()).get('group')
        if subject.title() in subjects_teacher.split(', '):
            await state.update_data(subject=subject.title())
            await message.answer('Введите <b>один из ваших отделений</b>, по которому собираетесь получить сведения:',
                                 reply_markup=OnePlus(
                                     text=group_teacher.split('/'),
                                 ).reply_keyboard)
            await TeachersUpdates.next()
        else:
            await message.answer('Это <b>не ваш</b> предмет!')


@dp.message_handler(state=TeachersUpdates.change_group)
async def get_group(message: Message, state: FSMContext):
    group = message.text.upper()
    if group == '🔙НАЗАД' or group == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        group_teacher = (await state.get_data()).get('group')
        if group in group_teacher.split('/'):
            await state.update_data(group=group.upper())
            await message.answer('Выберите <b>номер</b> класса, у которого собираетесь получить сведения:',
                                 reply_markup=classroom_number)
            await TeachersUpdates.next()
        else:
            await message.answer('Это <b>не ваше</b> отделение!')


@dp.message_handler(state=TeachersUpdates.classroomNumber)
async def get_classroomNumber(message: Message, state: FSMContext):
    number = message.text.upper()
    if number == '🔙НАЗАД' or number == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if number in numbers_list:
            await state.update_data(classroomNumber=int(number))
            await message.answer('Выберите <b>букву</b> класса', reply_markup=classroom_letter)
            await TeachersUpdates.next()
        else:
            await message.answer('Пожалуйста выберите <b>число из списка</b>:', reply_markup=classroom_number)


@dp.message_handler(state=TeachersUpdates.classroomLetter)
async def get_classroomLetter(message: Message, state: FSMContext):
    letter = message.text.upper()
    data = await state.get_data()
    subject = data.get('subject')
    group = data.get('group')
    school = data.get('school')
    pargroup = data.get('pargroup')
    classroomNumber = data.get('classroomNumber')
    if letter == '🔙НАЗАД' or letter == 'НАЗАД':
        await state.finish()
        await message.answer('<b>Главное меню</b>\n'
                             'выберите действие с кнопок ниже\n\n'
                             'Доп. Информация: /help',
                             reply_markup=Teachers_buttons)
    else:
        if letter in letters_list:
            send = f'Сведения посещаемости {subject} в {classroomNumber}"{letter}":\n'
            logs = await db.exist_open_accepts_for_teachers(school=school, group=group, classroom_number=classroomNumber,
                                                            classroom_letter=letter, pargroup=pargroup, subject=subject,
                                                            id=message.from_user.id)
            if logs:
                students = await db.exist_students_accepts(school=school, group=group,
                                                           classroom_number=classroomNumber, classroom_letter=letter,
                                                           pargroup=pargroup, subject=subject)
                for data in students:
                    if data[0]:
                        send += f'{data[4]} {data[3]}: @{data[2]}\n'
                        await db.update_students_accepts(id=data[1], subject=subject, accept=False)
                await db.update_teacher_accepts(id=message.from_user.id, subject=subject, school=school,
                                                classroom_number=classroomNumber, classroom_letter=letter, group=group,
                                                pargroup=pargroup, accept=False)
                await message.answer(text=send, reply_markup=Teachers_buttons)
                await state.finish()
            else:
                if logs is None:
                    await db.add_teacher_accepts(id=message.from_user.id, username=message.from_user.username,
                                                 last_name='Учитель предмета', first_name=subject, school=school,
                                                 group=group, classroom_number=classroomNumber, classroom_letter=letter,
                                                 pargroup=pargroup, subject=subject, accepts=True)
                else:
                    await db.update_teacher_accepts(id=message.from_user.id, subject=subject, school=school,
                                                    classroom_number=classroomNumber, classroom_letter=letter, group=group,
                                                    pargroup=pargroup, accept=True)
                await message.answer(text=f'Ученики {classroomNumber}"{letter}" могут отметиться по предмету {subject}',
                                     reply_markup=Teachers_buttons)
            await state.finish()
        else:
            await message.answer('Пожалуйста выберите <b>букву из списка</b>:', reply_markup=classroom_letter)
