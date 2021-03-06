from io import BytesIO

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

from .access import AccessMiddleware
from .access import public as public_command
from .access import root_only
from .settings import BotSettings
from .templates import TemplatesManager

bot = Bot(token=BotSettings.token())
dp = Dispatcher(bot, storage=MemoryStorage())
templates_manager = TemplatesManager()


@dp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy.pop("template", None)  # Reset current user template

    await message.answer(
        "Привет. Это бот для создания шаблонных постеров Гражданского Общества. Отправь /templates "
        "чтобы получить список шаблонов"
    )


@dp.message_handler(commands=["templates"])
async def templates_list(message: types.Message):
    templates = templates_manager.all_templates()

    if not templates:
        await message.answer("В базе нет ни одного шаблона. Администратор может добавить шаблон командой /add")
        return

    for name, template in templates.items():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(f"Выбрать {name}", callback_data=name))
        await message.answer_photo(template.preview, reply_markup=keyboard)


@dp.message_handler(commands=["add"])
@root_only()
async def add_template(message: types.Message):
    await message.answer(
        f"Окей, отправь мне файл {templates_manager.template_format}. В описании к файлу можно "
        f"указать имя шаблона. По-умолчанию имя файла будет именем шаблона."
    )


@dp.message_handler(commands=["remove"])
@root_only()
async def remove_template(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        template = proxy.get("template", None)
        if not template:
            await message.answer("Сначала выберите шаблон в меню /templates")
        elif template not in templates_manager.all_templates():
            await message.answer(
                "Такого шаблона больше нет в списке шаблонов. Выберите другой шаблон из списка /templates"
            )
        else:
            # TODO: 'Are you sure?' question should be here
            templates_manager.remove_template(template)
            proxy.pop("template", None)  # Reset current user template
            await message.answer("Шаблон удалён")


@dp.message_handler(commands=["chat_id"])
@public_command()  # Everyone can call
async def get_chat_id(message: types.Message):
    """
    Get current chat ID (for privileges settings)
    :param message:
    :return:
    """
    await message.answer(message.chat.id)


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
@root_only()
async def receive_file(message: types.Message, state: FSMContext):
    name = message.document.file_name
    if not name.endswith(templates_manager.template_format):
        await message.answer(f"Принимаются только файлы {templates_manager.template_format}")
        return

    if message.caption:
        caption = message.caption.strip().lower().replace("\n", "_").replace(" ", "_")
        if not caption.endswith(templates_manager.template_format):
            caption += templates_manager.template_format
            name = caption

    if await templates_manager.add_template(message.document, name):
        await message.answer("Шаблон добавлен")
    else:
        await message.answer("Ошибка при чтении файла; попробуйте другой файл")


@dp.message_handler(content_types=["text"])
async def process_text(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        template = proxy.get("template", None)
        if not template:
            await message.answer("Сначала выберите шаблон в меню /templates")
        elif template not in templates_manager.all_templates():
            await message.answer(
                "Такого шаблона больше нет в списке шаблонов. Выберите другой шаблон из списка /templates"
            )
        else:
            await message.answer("Рисую плакат, ждите ... (до ~15 секунд)")
            preview, pdf = templates_manager.process_template(template, message.text)
            await message.answer_photo(preview)
            await message.answer_document(InputFile(BytesIO(pdf), filename=f"{template}_poster.pdf"))


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    template = callback_query.data
    if template not in templates_manager.all_templates():
        await bot.send_message(callback_query.from_user.id, "Такого шаблона не существует")
        return
    await bot.send_message(
        callback_query.from_user.id,
        f"Выбран шаблон {template}, теперь отправьте текст для плаката."
        f"\n\nЧтобы вернуться к списку шаблонов отправьте /templates",
    )
    async with state.proxy() as proxy:
        proxy["template"] = template


def main():
    dp.middleware.setup(AccessMiddleware(BotSettings.access_chat_id()))
    dp.loop.run_until_complete(templates_manager.update_templates())
    executor.start_polling(dp, skip_updates=True)
