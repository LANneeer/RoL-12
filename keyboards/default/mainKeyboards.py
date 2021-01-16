from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _

school_list = ['СОШ №3', 'СОШ №12']

numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

letters_list = ['ОГН', 'ЕМН', 'А', 'Ә', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л']

Back = _('🔙НАЗАД')


classroom_number = ReplyKeyboardMarkup(
    keyboard=[[
            KeyboardButton(text=numbers_list[9]),
            KeyboardButton(text=numbers_list[10])
        ],
        [
            KeyboardButton(text=numbers_list[6]),
            KeyboardButton(text=numbers_list[7]),
            KeyboardButton(text=numbers_list[8])
        ],
        [
            KeyboardButton(text=numbers_list[3]),
            KeyboardButton(text=numbers_list[4]),
            KeyboardButton(text=numbers_list[5])
        ],
        [
            KeyboardButton(text=numbers_list[0]),
            KeyboardButton(text=numbers_list[1]),
            KeyboardButton(text=numbers_list[2])
        ],
        [
            KeyboardButton(text=Back)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
classroom_letter = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text=letters_list[0]),
        KeyboardButton(text=letters_list[1])
    ],
        [
            KeyboardButton(text=letters_list[2]),
            KeyboardButton(text=letters_list[3]),
            KeyboardButton(text=letters_list[4])
        ],
        [
            KeyboardButton(text=letters_list[5]),
            KeyboardButton(text=letters_list[6]),
            KeyboardButton(text=letters_list[7])
        ],
        [
            KeyboardButton(text=letters_list[8]),
            KeyboardButton(text=letters_list[9]),
            KeyboardButton(text=letters_list[10])
        ],
        [
            KeyboardButton(text=letters_list[11]),
            KeyboardButton(text=letters_list[12]),
            KeyboardButton(text=letters_list[13])
        ],
        [
            KeyboardButton(text=Back)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=Back)], ],
    resize_keyboard=True,
    one_time_keyboard=True
)
back_and_send = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=_('СДАТЬ'))],
        [KeyboardButton(text=Back)]
    ],
    resize_keyboard=True
)

yes_or_no = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=_('Да'))],
        [KeyboardButton(text=_('Нет'))]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
