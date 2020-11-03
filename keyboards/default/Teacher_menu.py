from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Teachers_buttons = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='Отправить задания 📤'),
        KeyboardButton(text='Получить работы 📥')
    ],
        [
            KeyboardButton(text='Создать объявление ✏️'),
            KeyboardButton(text='Сведения о работах 📎')
        ],
        [
            KeyboardButton(text='Открыть урок ⏰')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
