from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

classroom_number = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='10'),
        KeyboardButton(text='11')
    ],
        [
            KeyboardButton(text='7'),
            KeyboardButton(text='8'),
            KeyboardButton(text='9')
        ],
        [
            KeyboardButton(text='4'),
            KeyboardButton(text='5'),
            KeyboardButton(text='6')
        ],
        [
            KeyboardButton(text='1'),
            KeyboardButton(text='2'),
            KeyboardButton(text='3')
        ],
        [
            KeyboardButton(text='🔙НАЗАД')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
classroom_letter = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='ОГН'),
        KeyboardButton(text='ЕМН')
    ],
        [
            KeyboardButton(text='А'),
            KeyboardButton(text='Ә'),
            KeyboardButton(text='Б')
        ],
        [
            KeyboardButton(text='В'),
            KeyboardButton(text='Г'),
            KeyboardButton(text='Д')
        ],
        [
            KeyboardButton(text='Е'),
            KeyboardButton(text='Ж'),
            KeyboardButton(text='З')
        ],
        [
            KeyboardButton(text='И'),
            KeyboardButton(text='К'),
            KeyboardButton(text='Л')
        ],
        [
            KeyboardButton(text='🔙НАЗАД')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='🔙НАЗАД')], ],
    resize_keyboard=True,
    one_time_keyboard=True
)
back_and_send = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='СДАТЬ')],
        [KeyboardButton(text='🔙НАЗАД')]
    ],
    resize_keyboard=True
)

yes_or_no = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да')],
        [KeyboardButton(text='Нет')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

school_list = ['СОШ №3', 'СОШ №12']

numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

letters_list = ['ОГН', 'ЕМН', 'А', 'Ә', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л']
