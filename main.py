import math
import random

from aiogram.types import User
from aiogram.utils.executor import start_webhook

import database as DB
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import config
import logging
import aiogram

from database import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

DB = Database('db.db')


@dp.message_handler(commands=['add_quote'])
async def add_quote(message: types.Message):
    if message.reply_to_message == None:
        await message.answer("Не втрана циаиа")
    else:
        DB.add_quote(message.reply_to_message.from_user.id, message.reply_to_message.text,
                     message.reply_to_message.from_user.username)
        await message.answer("Цитата добалена")


@dp.message_handler(commands=['random_quote'])
async def add_quote(message: types.Message):
    data = DB.get_all_quotes()
    var = data[math.floor(random.random() * len(data))]
    await message.answer("Випадкова цитата:\n" + var[2] + "\nby @" + var[3])


@dp.message_handler(commands=['random_quote_by_user'])
async def add_quote(message: types.Message):
    if message.reply_to_message == None:
        await message.answer("Чия цитата, дібіл. Чорним по чортому написано BY_USER.")
    else:
        data = DB.get_quotes_by_user_id(message.reply_to_message.from_user.id)
        if len(data) == 0:
            await message.answer("Цитат нема, юзер бидло.")
        else:
            var = data[math.floor(random.random() * len(data))]
            await message.answer("Випадкова цитата:\n" + var[2] + "\nby @" + var[3])


async def on_startup(dp):
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT, )
