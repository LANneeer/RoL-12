from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class Students(BoundFilter):
    async def check(self, message: types.Message):
        if await db.exist_student(message.from_user.id):
            return True


class Teacher(BoundFilter):
    async def check(self, message: types.Message):
        if await db.exist_teacher(message.from_user.id):
            return True


class Ban(BoundFilter):
    async def check(self, message: types.Message):
        if not await db.exists_ban(message.from_user.id):
            return True
