from aiogram import Dispatcher

from .special_filters import Students
from .special_filters import Teacher
from .special_filters import Ban


def setup(dp: Dispatcher):
    dp.filters_factory.bind(Students)
    dp.filters_factory.bind(Teacher)
    dp.filters_factory.bind(Ban)