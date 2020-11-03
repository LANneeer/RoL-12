from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Subject_buttons = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='Алгебра'),
        KeyboardButton(text='Физика'),
        KeyboardButton(text='Геометрия')
    ],
        [
            KeyboardButton(text='Химия'),
            KeyboardButton(text='Биология'),
            KeyboardButton(text='Информатика')
        ],
        [
            KeyboardButton(text='История Казахстана'),
            KeyboardButton(text='История Мира'),
            KeyboardButton(text='ЧОП')
        ],
        [
            KeyboardButton(text='География'),
            KeyboardButton(text='Казахский Язык/Литература'),
            KeyboardButton(text='Самопознание')
        ],
        [
            KeyboardButton(text='Русский Язык'),
            KeyboardButton(text='Русская Литература'),
            KeyboardButton(text='Английский Язык'),
        ],
        [
            KeyboardButton(text='Технология/мужской'),
            KeyboardButton(text='Технология/женский'),
            KeyboardButton(text='Естествознание')
        ],
        [
          KeyboardButton(text='🔙НАЗАД')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

Group_buttons = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='KZ'), KeyboardButton(text='RU')],
              [KeyboardButton(text='🔙НАЗАД')]],
    resize_keyboard=True,
    one_time_keyboard=True
)

Group_buttons_teacher = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='KZ'), KeyboardButton(text='RU')],
              [KeyboardButton(text='KZ/RU')],
              [KeyboardButton(text='🔙НАЗАД')]],
    resize_keyboard=True,
    one_time_keyboard=True
)

Pargroup_buttons_teacher = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='0')],
              [KeyboardButton(text='1'), KeyboardButton(text='2')],
              [KeyboardButton(text='🔙НАЗАД')]],
    resize_keyboard=True,
    one_time_keyboard=True
)

Pargroup_buttons = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='1'), KeyboardButton(text='2')],
              [KeyboardButton(text='🔙НАЗАД')]],
    resize_keyboard=True,
    one_time_keyboard=True
)


subjects_list = ['АЛГЕБРА', 'ФИЗИКА', 'ГЕОМЕТРИЯ', 'ИНФОРМАТИКА',
                 'БИОЛОГИЯ', 'ИСТОРИЯ КАЗАХСТАНА', 'ИСТОРИЯ МИРА', 'ЧОП', 'ГЕОГРАФИЯ',
                 'ТЕХНОЛОГИЯ/МУЖСКОЙ', 'ТЕХНОЛОГИЯ/ЖЕНСКИЙ', 'САМОПОЗНАНИЕ', 'РУССКИЙ ЯЗЫК', 'РУССКАЯ ЛИТЕРАТУРА',
                 'АНГЛИЙСКИЙ ЯЗЫК', 'КАЗАХСКИЙ ЯЗЫК/ЛИТЕРАТУРА', 'ЕСТЕСТВОЗНАНИЕ', 'ХИМИЯ']

groups_list = ['KZ', 'RU']

groups_list_teacher = ['KZ', 'RU', 'KZ/RU']

pargroup_list = ['0', '1', '2']