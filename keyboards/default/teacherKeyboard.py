from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _

Teachers_buttons = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text=_('Отправить задания 📤')),
        KeyboardButton(text=_('Получить работы 📥'))
    ],
        [
            KeyboardButton(text=_('Создать объявление ✏️')),
            KeyboardButton(text=_('Сведения о работах 📎'))
        ],
        [
            KeyboardButton(text=_('Открыть урок ⏰'))
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
