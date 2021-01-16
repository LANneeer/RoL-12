from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _

groups_list = ['KZ', 'RU']

groups_list_teacher = ['KZ', 'RU', 'KZ/RU']

pargroup_list = ['0', '1', '2']

Back = _('🔙НАЗАД')

subjects_list = ['АЛГЕБРА', 'ФИЗИКА', 'ГЕОМЕТРИЯ', 'ИНФОРМАТИКА',
                 'БИОЛОГИЯ', 'ИСТОРИЯ КАЗАХСТАНА', 'ИСТОРИЯ МИРА', 'ЧОП', 'ГЕОГРАФИЯ',
                 'ТЕХНОЛОГИЯ/МУЖСКОЙ', 'ТЕХНОЛОГИЯ/ЖЕНСКИЙ', 'САМОПОЗНАНИЕ', 'РУССКИЙ ЯЗЫК', 'РУССКАЯ ЛИТЕРАТУРА',
                 'АНГЛИЙСКИЙ ЯЗЫК', 'КАЗАХСКИЙ ЯЗЫК/ЛИТЕРАТУРА', 'ЕСТЕСТВОЗНАНИЕ', 'ХИМИЯ']


Subject_buttons = ReplyKeyboardMarkup(
    keyboard=[[
            KeyboardButton(text=subjects_list[0]),
            KeyboardButton(text=subjects_list[1]),
            KeyboardButton(text=subjects_list[2])
        ],
        [
            KeyboardButton(text=subjects_list[17]),
            KeyboardButton(text=subjects_list[4]),
            KeyboardButton(text=subjects_list[3])
        ],
        [
            KeyboardButton(text=subjects_list[5]),
            KeyboardButton(text=subjects_list[6]),
            KeyboardButton(text=subjects_list[7])
        ],
        [
            KeyboardButton(text=subjects_list[8]),
            KeyboardButton(text=subjects_list[15]),
            KeyboardButton(text=subjects_list[11])
        ],
        [
            KeyboardButton(text=subjects_list[12]),
            KeyboardButton(text=subjects_list[13]),
            KeyboardButton(text=subjects_list[14]),
        ],
        [
            KeyboardButton(text=subjects_list[9]),
            KeyboardButton(text=subjects_list[10]),
            KeyboardButton(text=subjects_list[16])
        ],
        [
          KeyboardButton(text=_('🔙НАЗАД'))
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

Group_buttons = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='KZ'), KeyboardButton(text='RU')],
              [KeyboardButton(text=Back)]],
    resize_keyboard=True,
    one_time_keyboard=True
)

Group_buttons_teacher = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='KZ'), KeyboardButton(text='RU')],
              [KeyboardButton(text='KZ/RU')],
              [KeyboardButton(text=Back)]],
    resize_keyboard=True,
    one_time_keyboard=True
)

Pargroup_buttons_teacher = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=pargroup_list[0])],
              [KeyboardButton(text=pargroup_list[1]), KeyboardButton(text=pargroup_list[2])],
              [KeyboardButton(text=Back)]],
    resize_keyboard=True,
    one_time_keyboard=True
)

Pargroup_buttons = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=pargroup_list[1]), KeyboardButton(text=pargroup_list[2])],
              [KeyboardButton(text=Back)]],
    resize_keyboard=True,
    one_time_keyboard=True
)
