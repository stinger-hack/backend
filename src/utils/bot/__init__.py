from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from aiogram import Bot, Dispatcher, executor, types
from settings import BOT_API_KEY
from services.db import DB
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=BOT_API_KEY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()


async def check_user_telegram(telegram_id: int):
    query = """
        select exists (
            select
            from users
            where telegram_id = $1
        )
    """
    result = await DB.conn.fetchrow(query, telegram_id)
    return result


async def add_user_telegram(email: str, telegram_id):
    query = """
        update users
        set telegram_id = $1
        where email = $2
    """
    result = await DB.conn.fetchrow(query, telegram_id, email)
    return result

@dp.message_handler(Text(equals='pavel@mail.ru', ignore_case=True), state='*')
async def process_age_invalid(message: types.Message):
    """
    If age is invalid
    """
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    text_and_data = (
        ('Избранное', 'favorite'),
        ('Профиль', 'profile'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup.row(*row_btns)
    keyboard_markup.add(
        types.InlineKeyboardButton('Наш сайт', url='https://stinger-hack.ru'),
    )
    return await message.reply("Привет, Павел", reply_markup=keyboard_markup)


# @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
# async def process_age_invalid(message: types.Message):
#     """
#     If age is invalid
#     """
#     return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")

# @dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['^@*']))
# async def send_welcome(message: types.Message, regexp_command):
#     await message.reply("base")


@dp.message_handler(commands="start")
async def dp_start(message: types.Message):
    user: dict = await check_user_telegram(message.from_user.id)
    if user['exists']:
        return await message.reply("Привет, Павел")
    return await message.reply("Ваш телеграм не найден, введите email")


async def init_db():
    await DB.connect()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    executor.start_polling(dp, skip_updates=True)
