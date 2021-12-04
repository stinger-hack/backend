from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from settings import BOT_API_KEY
from services.db import DB
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from services.feed import get_news_service
from src.services.get_favorites import get_favorites_service

bot = Bot(token=BOT_API_KEY, parse_mode='Markdown')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    email = State()


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


async def get_first_name(telegram_id: int):
    query = """
        select first_name
        from users
        where telegram_id = $1
    """
    result = await DB.conn.fetchrow(query, telegram_id)
    return result['first_name']


async def add_user_telegram(email: str, telegram_id):
    query = """
        update users
        set telegram_id = $1
        where email = $2
    """
    result = await DB.conn.fetchrow(query, telegram_id, email)
    return result


@dp.message_handler(commands="start")
async def dp_start(message: types.Message):
    user: dict = await check_user_telegram(message.from_user.id)

    if user['exists']:
        first_name = await get_first_name(telegram_id=message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Избранное", "Новости")
        markup.add("Сообщения")
        return await message.reply(f"Привет, {first_name}", reply_markup=markup)

    await Form.email.set()
    return await message.reply("Ваш телеграм не найден, введите email")


@dp.message_handler(state=Form.email)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Избранное", "Новости")
    markup.add("Сообщения")

    await message.reply("Теперь ваш телеграм привязан к аккаунту", reply_markup=markup)


@dp.message_handler(filters.Text(equals='Избранное'))
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Сообщения", "Новости")

    result = await get_favorites_service()

    msg_text = ''

    for item in result:
        msg_text += f"*{item['project_name']}* \n"
        msg_text += f"_{item['description']}_ \n \n"

    await message.reply(msg_text, reply_markup=markup)


@dp.message_handler(filters.Text(equals='Сообщения'))
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Избранное", "Новости")

    await message.reply("Список сообщений пуст", reply_markup=markup)


@dp.message_handler(filters.Text(equals='Новости'))
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Сообщения", "Избранное")

    msg_text = ''

    result = await get_news_service()

    for item in result:
        msg_text += f"*{item['news_header']}* \n"
        msg_text += f"_{item['news_text']}_ \n \n"

    await message.reply(msg_text, reply_markup=markup)


async def init_db():
    await DB.connect()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    executor.start_polling(dp, skip_updates=True)
