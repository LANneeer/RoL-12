from aiogram import Dispatcher
from .specialFilters import Students, Teacher, Ban


def setup(dp: Dispatcher):
    dp.filters_factory.bind(Students)
    dp.filters_factory.bind(Teacher)
    dp.filters_factory.bind(Ban)
