import typing
from dataclasses import dataclass

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


@dataclass
class OnePlus:
    text: typing.List
    aling: typing.List[int] = None

    @property
    def reply_keyboard(self):
        return oneplus_keyboard(self)


def oneplus_keyboard(args: OnePlus) -> ReplyKeyboardMarkup:  # означает что выводит ReplyKeyboardMarkup
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if not args.aling:
        for num, button in enumerate(args.text):
            keyboard.add(KeyboardButton(text=str(button)))
    else:
        count = 0
        for row_size in args.aling:
            keyboard.row(*[KeyboardButton(text=str(text)) for text in args.text[count: count + row_size]])
            count += row_size
    return keyboard
