from loader import bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.default import classroom_number, classroom_letter, Subject_buttons, Group_buttons, Students_buttons, \
    Teachers_buttons, Group_buttons_teacher, OnePlus
from keyboards.default.mainKeyboards import numbers_list, letters_list, yes_or_no, school_list
from keyboards.default.subjectsKeyboard import subjects_list, groups_list, pargroup_list, Pargroup_buttons, \
    Pargroup_buttons_teacher, groups_list_teacher, Back
from loader import dp, db, _
from states.mainStates import StudentsRegister, TeacherRegister


# STUDENTS REGISTRATION
# Приём фамилии и имени
@dp.message_handler(state=StudentsRegister.user_name)
async def get_students_name(message: Message, state: FSMContext):
    answer = message.text
    try:
        if len(answer) < 65:
            last_name, first_name = answer.split()
            if last_name.isalpha() and first_name.isalpha():
                await state.update_data(first_name=first_name.title(), last_name=last_name.title())
                await message.answer(text=_('Выберите вашу школу:'),
                                     reply_markup=OnePlus(text=school_list).reply_keyboard)
                await StudentsRegister.next()
            else:
                await message.answer(_('Вы ввели <b>фамилию и имя</b> в неправильном формате!\n'
                                       'Введите <b>фамилию и имя <u>через пробел</u></b>:'))
        else:
            await message.answer(_('Слишком длинная фамилия/имя'))
    except (ValueError, TypeError):
        await message.answer(_('Вы ввели <b>фамилию и имя</b> в неправильном формате!\n'
                               'Введите <b>фамилию и имя <u>через пробел</u></b>:'))


# Выбор школы
@dp.message_handler(state=StudentsRegister.school)
async def get_students_school(message: Message, state: FSMContext):
    answer = str(message.text).upper()
    if answer in school_list:
        await state.update_data(school=answer)
        await message.answer(_('Выберите <u>отделение</u> вашего класса:'), reply_markup=Group_buttons)
        await StudentsRegister.next()
    else:
        await message.answer(_('Такой <b>школы нету</b> в списке!\nВыберите школу из <b>списка</b>!'))


# Выбор группы
@dp.message_handler(state=StudentsRegister.group)
async def get_students_group(message: Message, state: FSMContext):
    group = message.text.upper()
    if group == Back or group == Back[1:]:
        await StudentsRegister.user_name.set()
        await message.answer(_('Введите вашу <b><u>фамилию и имя</u></b>'))
    else:
        if group in groups_list:
            await state.update_data(group=group)
            await message.answer(_('Выберите <u>номер</u> вашего класса:'), reply_markup=classroom_number)
            await StudentsRegister.next()
        else:
            await message.answer(_('Выберите <b>отделение</b> из списка!'))


# Приём цифры класса
@dp.message_handler(state=StudentsRegister.classroomNumber)
async def get_students_number(message: Message, state: FSMContext):
    number = message.text
    if number.upper() == Back or number.upper() == Back[1:]:
        await StudentsRegister.group.set()
        await message.answer(_('Выберите <u>отделение</u> вашего класса:'), reply_markup=Group_buttons)
    else:
        if number in numbers_list:
            await state.update_data(classroomNumber=number)
            await message.answer(_('Выберите <u>букву</u> вашего класса:'), reply_markup=classroom_letter)
            await StudentsRegister.next()
        else:
            await message.answer(_('Пожалуйста введите <b>число</b> вашего класса:'), reply_markup=classroom_number)


# Приём буквы класса
@dp.message_handler(state=StudentsRegister.classroomLetter)
async def get_students_letter(message: Message, state: FSMContext):
    letter = message.text.upper()
    if letter == Back or letter == Back[1:]:
        await StudentsRegister.classroomNumber.set()
        await message.answer(_('Выберите <u>номер</u> вашего класса:'), reply_markup=classroom_number)
    else:
        if letter in letters_list:
            await state.update_data(classroomLetter=letter)
            await message.answer(_('Выберите вашу <b>пар-группу</b>'), reply_markup=Pargroup_buttons)
            await StudentsRegister.next()
        else:
            await message.answer(_('Введите <b>букву из списка</b>'))


# Прием паргруппы
@dp.message_handler(state=StudentsRegister.pargroup)
async def get_students_pargroup(message: Message, state: FSMContext):
    pargroup = message.text.upper()
    if pargroup == Back or pargroup == Back[1:]:
        await StudentsRegister.classroomLetter.set()
        await message.answer(_('Выберите <u>букву</u> вашего класса:'), reply_markup=classroom_letter)
    else:
        if pargroup in pargroup_list:
            if message.from_user.username is None:
                await message.answer(_('Зачем ты удалил своё имя пользователя?! Регистрируйся заново как и начал!'))
                await StudentsRegister.user_name.set()
                await message.answer(_('Введите вашу <b><u>фамилию и имя</u></b>'))
            else:
                data = await state.get_data()
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                school = data.get('school')
                group = data.get('group')
                classroomNumber = data.get('classroomNumber')
                classroomLetter = data.get('classroomLetter')
                await state.update_data(pargroup=pargroup)
                await state.update_data(username=message.from_user.username)
                await StudentsRegister.next()
                await message.answer(_('Имя: {first_name}\nФамилия: {last_name}\n'
                                       'Школа: {school}\n'
                                       'Отделение: {group}\nКласс: {classroomNumber} "{classroomLetter}"\n'
                                       'Пар-группа: {pargroup}\n'
                                       'Ваше имя пользователя: @{username}\n\n'
                                       'Всё ли введено верно?').format(first_name=first_name, last_name=last_name,
                                                                       school=school, group=group, pargroup=pargroup,
                                                                       classroomNumber=classroomNumber,
                                                                       classroomLetter=classroomLetter,
                                                                       username=message.from_user.username),
                                     reply_markup=yes_or_no)
        else:
            await message.answer(_('Выберите <b>пар-группу</b> из списка!'), reply_markup=Pargroup_buttons)


# Подтверждение!
@dp.message_handler(state=StudentsRegister.accept)
async def get_students_accept(message: Message, state: FSMContext):
    data = await state.get_data()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    school = data.get('school')
    group = data.get('group')
    classroomNumber = data.get('classroomNumber')
    classroomLetter = data.get('classroomLetter')
    pargroup = data.get('pargroup')
    username = data.get('username')
    if message.text.upper() == _('ДА'):
        await db.add_students(id=message.from_user.id, username=username,
                              first_name=first_name,
                              last_name=last_name, school=school, groups=group,
                              classroom_number=int(classroomNumber), classroom_letter=classroomLetter,
                              pargroup=int(pargroup))
        await bot.send_photo(chat_id=message.from_user.id,
                             photo='https://i.ibb.co/KGHt21B/photo-2020-08-22-00-20-52.jpg',
                             caption=_('Вы успешно внесены в базу данных!\n\n'
                                       'Если у вас не появились кнопки снизу, то нажмите на '
                                       'эту кнопку возле ввода текста\n\n'
                                       '<b>Так-же не думайте кидать иной контент по мимо учебного!\n'
                                       '(мы спокойно можем связаться с вами по номеру телефона :3)</b>'),
                             reply_markup=Students_buttons)
        await state.finish()
    elif message.text.upper() == _('НЕТ'):
        await message.answer(_('Введите вашу <b><u>фамилию и имя</u></b>'), reply_markup=ReplyKeyboardRemove())
        await StudentsRegister.user_name.set()
    else:
        await message.answer(_('<b>Вы не ответили на вопрос!</b>'), reply_markup=yes_or_no)


# TEACHER REGISTRATION
# Приём фамилии и имени учителя
@dp.message_handler(state=TeacherRegister.user_name)
async def get_teachers_name(message: Message, state: FSMContext):
    answer = message.text
    try:
        if len(answer) < 65:
            last_name, first_name = answer.split()
            if last_name.isalpha() and first_name.isalpha():
                await state.update_data(first_name=first_name.title(), last_name=last_name.title())
                await message.answer(text=_('Выберите вашу школу:'),
                                     reply_markup=OnePlus(text=school_list).reply_keyboard)
                await TeacherRegister.next()
            else:
                await message.answer(_('Вы ввели <b>фамилию и имя</b> в неправильном формате!\n'
                                     'Введите <b>фамилию и имя <u>через пробел</u></b>:'))
        else:
            await message.answer(_('Слишком длинная фамилия/имя'))
    except (ValueError, TypeError):
        await message.answer(_('вы ввели <u>фамилию и имя</u> в неправильном формате!\n'
                             'введите <b>фамилию и имя <u>через пробел</u></b>:'))


# Выбор школы
@dp.message_handler(state=TeacherRegister.school)
async def get_teacher_school(message: Message, state: FSMContext):
    answer = str(message.text).upper()
    if answer in school_list:
        await state.update_data(school=answer)
        await message.answer(_('Выберите <u>отделение</u> вашего предмета:'), reply_markup=Group_buttons_teacher)
        await TeacherRegister.next()
    else:
        await message.answer(_('Такой <b>школы нету</b> в списке!\nВыберите школу из <b>списка</b>!'))


# Выбор группы
@dp.message_handler(state=TeacherRegister.group)
async def get_teacher_group(message: Message, state: FSMContext):
    group = message.text.upper()
    if group == Back or group == Back[1:]:
        await TeacherRegister.user_name.set()
        await message.answer(_('Введите вашу <b><u>фамилию и имя</u></b>'))
    else:
        if group in groups_list_teacher:
            await state.update_data(group=group)
            await message.answer(_('Выберите <u>название</u> вашего предмета:\n\n'
                                   '<b><u>Если у вас более одного предмета '
                                   'вам надо ввеcти их в ручную и через запятую</u></b>'),
                                 reply_markup=Subject_buttons)
            await TeacherRegister.next()
        else:
            await message.answer(_('Выберите <u>отделение</u> из списка!'))


# Приём предметов учителя
@dp.message_handler(state=TeacherRegister.user_subject)
async def get_teacher_group(message: Message, state: FSMContext):
    teacher_subjects = message.text.upper()
    if teacher_subjects == Back or teacher_subjects == Back[1:]:
        await TeacherRegister.group.set()
        await message.answer(_('Выберите <u>отделение</u> вашего предмета:'), reply_markup=Group_buttons_teacher)
    else:
        teacher_subjects = ', '.join(map(lambda x: x.strip(), teacher_subjects.split(',')))
        if len(set(teacher_subjects.split(', ') + subjects_list)) == len(subjects_list):
            await state.update_data(teacher_subjects=teacher_subjects.title())
            await TeacherRegister.next()
            await message.answer(_('Выберите вашу <b>пар-группу</b>\n'
                                   '<b>Выберите "0" если ни один из ваших предметов не делится на паргруппы, '
                                   'или вы ведете его один</b>'),
                                 reply_markup=Pargroup_buttons_teacher)
        else:
            await message.answer('Введите предмет который есть в кнопках!', reply_markup=Subject_buttons)


# Прием паргруппы
@dp.message_handler(state=TeacherRegister.pargroup)
async def get_teacherss_pargroup(message: Message, state: FSMContext):
    pargroup = message.text.upper()
    if pargroup == Back or pargroup == Back[1:]:
        await TeacherRegister.user_subject.set()
        await message.answer(_('Выберите <u>название</u> вашего предмета:\n\n'
                               '<b><u>Если у вас более одного предмета '
                               'вам надо ввеcти их в ручную и через запятую</u></b>'),
                             reply_markup=Subject_buttons)
    else:
        if pargroup in pargroup_list:
            if message.from_user.username is None:
                await message.answer(_('Зачем ты удалил своё имя пользователя?! Регистрируйся заново как и начал!'))
                await TeacherRegister.user_name.set()
                await message.answer(_('Введите вашу <b><u>фамилию и имя</u></b>'))
            else:
                data = await state.get_data()
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                school = data.get('school')
                group = data.get('group')
                teacher_subjects = data.get('teacher_subjects')
                await state.update_data(pargroup=pargroup)
                await state.update_data(username=message.from_user.username)
                await TeacherRegister.next()
                await message.answer(_('Имя: {first_name}\nФамилия: {last_name}\n'
                                       'Школа: {school}\n'
                                       'Отделение: {group}\nПредметы: {teacher_subjects}\nПар-группа: {pargroup}\n'
                                       'Ваше имя пользователя: @{username}\n\n'
                                       'Всё ли введено верно?').format(first_name=first_name, last_name=last_name,
                                                                       school=school, group=group,
                                                                       teacher_subjects=teacher_subjects,
                                                                       pargroup=pargroup,
                                                                       username=message.from_user.username),
                                     reply_markup=yes_or_no)
        else:
            await message.answer(_('Выберите <b>пар-группу</b> из списка!'), reply_markup=Pargroup_buttons_teacher)


# Подтверждение!
@dp.message_handler(state=TeacherRegister.accept)
async def get_teachers_subjects(message: Message, state: FSMContext):
    data = await state.get_data()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    school = data.get('school')
    group = data.get('group')
    teacher_subjects = data.get('teacher_subjects')
    pargroup = data.get('pargroup')
    username = data.get('username')
    if message.text.upper() == _('ДА'):
        await db.add_teachers(id=message.from_user.id, username=username,
                              first_name=first_name,
                              last_name=last_name, school=school, groups=group,
                              subject=teacher_subjects, pargroup=int(pargroup))
        await bot.send_photo(chat_id=message.from_user.id,
                             photo='https://i.ibb.co/KGHt21B/photo-2020-08-22-00-20-52.jpg',
                             caption=_('Вы успешно внесены в базу данных!\n\n'
                                       'Если у вас не появились кнопки снизу, то нажмите на '
                                       'эту кнопку возле ввода текста'),
                             reply_markup=Teachers_buttons)
        await state.finish()
    elif message.text.upper() == _('НЕТ'):
        await message.answer(_('Введите вашу <b><u>фамилию и имя</u></b>'), reply_markup=ReplyKeyboardRemove())
        await TeacherRegister.user_name.set()
    else:
        await message.answer(_('<b>Вы не ответили на вопрос!</b>'), reply_markup=yes_or_no)
