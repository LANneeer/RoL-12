from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from middlewares.language import setup_middleware
from config import const
from utils.database.pg_database import Database

bot = Bot(token=const.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(loop=dp.loop)

i18n = setup_middleware(dp)
_ = i18n.gettext
