from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Students_buttons = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='Сдать задание 📤'),
        KeyboardButton(text='Вопрос к учителю ℹ️'),
        KeyboardButton(text='Узнать задание 📥')
        ],
        [
        KeyboardButton(text='Отметиться на уроке ❗️')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
