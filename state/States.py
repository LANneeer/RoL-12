from aiogram.dispatcher.filters.state import StatesGroup, State


class StudentsRegister(StatesGroup):
    user_name = State()
    school = State()
    group = State()
    classroomNumber = State()
    classroomLetter = State()
    pargroup = State()
    accept = State()


class TeacherRegister(StatesGroup):
    user_name = State()
    school = State()
    group = State()
    user_subject = State()
    pargroup = State()
    accept = State()


class SendWork(StatesGroup):
    change_subject = State()
    change_group = State()
    classroomNumber = State()
    classroomLetter = State()
    files_id = State()


class GetWork(StatesGroup):
    change_subject = State()
    change_group = State()
    classroomNumber = State()
    classroomLetter = State()


class Advert(StatesGroup):
    change_subject = State()
    change_group = State()
    classroomNumber = State()
    classroomLetter = State()
    messages = State()


class TellWork(StatesGroup):
    change_subject = State()
    change_group = State()
    classroomNumber = State()
    classroomLetter = State()


class StudentsState(StatesGroup):
    view_doc = State()
    send_doc = State()
    send_doc2 = State()


class StudentsUpdates(StatesGroup):
    change_subject = State()
    Another = State()
    accept = State()


class TeachersUpdates(StatesGroup):
    change_subject = State()
    change_group = State()
    classroomNumber = State()
    classroomLetter = State()
