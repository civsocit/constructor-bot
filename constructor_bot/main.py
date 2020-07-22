from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .settings import BotSettings
from .templates import TemplatesManager


bot = Bot(token=BotSettings.token())
dp = Dispatcher(bot, storage=MemoryStorage())
templates_manager = TemplatesManager()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет. Это бот для создания шаблонных постеров Гражданского Общества")
    await message.answer("Выбери шаблон из набора шаблонов")

    await templates_manager.update_templates()

    templates = templates_manager.all_templates()

    for name, template in templates.items():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(name, callback_data=name))
        await message.answer_photo(template, reply_markup=keyboard)


@dp.message_handler(content_types=["text"])
async def process_text(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        template = proxy.get('template', 0)
        await message.answer_photo(templates_manager.process_template(template, message.text))


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Выбран шаблон {callback_query.data}, теперь отправьте текст "
                                                        f"для шаблона ('отмена' для отмены)")
    async with state.proxy() as proxy:
        proxy['template'] = callback_query.data


def main():
    executor.start_polling(dp, skip_updates=True)
