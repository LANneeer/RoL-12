from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types
from config.const import I18N_DOMAIN, LOCALES_DIR


async def get_language(id):
    '''
    Перекинуть эту функцию для работы с FSM
    '''
    return None


class ACLMiddleware(I18nMiddleware):
    '''
    Тут мы создаем класс что-бы автоматически находить язык
    по идее можно убрать (так и сделаю)
    хотя его можно изменить :D
    '''
    def get_user_locale(self, action, args):
        user = types.User.get_current()
        return get_language(user.id) or user.locale


def setup_middleware(dp):
    i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
