from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _

Students_buttons = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text=_('Сдать задание 📤')),
        KeyboardButton(text=_('Вопрос к учителю ℹ️')),
        KeyboardButton(text=_('Узнать задание 📥'))
        ],
        [
        KeyboardButton(text=_('Отметиться на уроке ❗️'))
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
