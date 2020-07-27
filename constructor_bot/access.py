import aiogram.types as types
from aiogram import Bot
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_chat_id: int):
        self._access_chat_id = access_chat_id
        super(AccessMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        bot = Bot.get_current()
        chat_member = await bot.get_chat_member(self._access_chat_id, message.from_user.id)
        if not chat_member.is_chat_member():
            await message.answer(f"Вы должны быть участником тематического чата для доступа к Конструктору Плакатов")
            raise CancelHandler()
