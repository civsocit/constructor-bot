import aiogram.types as types
from aiocache import cached
from aiogram import Bot
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from constructor_bot.settings import BotSettings


@cached(ttl=BotSettings.access_cache_ttl())
async def _check_user(user_id: int, chat_id: int) -> bool:
    """
    Check user access
    :param user_id: user id
    :param chat_id: access chat id
    :return: bool (yes\no)
    """
    bot = Bot.get_current()
    chat_member = await bot.get_chat_member(chat_id, user_id)
    return chat_member.is_chat_member()


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_chat_id: int):
        self._access_chat_id = access_chat_id
        super(AccessMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if message.chat.id < 0:  # Group chats are not allowed
            await message.answer("Для общения с ботом используйте личные сообщения")
            raise CancelHandler()

        if not await _check_user(message.from_user.id, self._access_chat_id):
            await message.answer("Вы должны быть участником тематического чата для доступа к Конструктору Плакатов")
            raise CancelHandler()
