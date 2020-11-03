import logging

from loader import db

# задаем логи для того что-бы код дебажить
logging.basicConfig(level=logging.INFO)


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)  # Устанавливает фильтры
    middlewares.setup(dp)  # Устанавливает middleware
    await db.create_table()  # Создает базу данных


# запуск лонгполлинга
if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    # dp=dispatcher(диспетчер с помощью которого происходит обработка сообщений),
    # on_startup=фунция которая запускается при старте,
    # skip_updates=пропустить старые входящие обновления
