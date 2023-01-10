import asyncio
import logging
import os

from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import filters

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot = Bot(str(os.getenv('TOKEN')))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_main(message: types.Message):
    print(message.chat.id)

    bot_message = await bot.send_message(message.chat.id, 'Bot is active')

    await asyncio.sleep(3)

    await bot.delete_message(message.chat.id, bot_message.message_id)
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(filters.Command(['of']), filters.AdminFilter())
async def listen_of(message: types.Message):
    msg = f"Who sent offtopic: @{message.from_user.username} \nUser from: @{message.reply_to_message.from_user.username}\n" + message.reply_to_message.text
    await bot.send_message(int(os.getenv('ID_OFFTOP')), msg)

    await bot.delete_message(message.chat.id, message.message_id)
    await bot.delete_message(message.chat.id, message.reply_to_message.message_id)

    msg = f"@{message.reply_to_message.from_user.username}, Your message has been sent @{message.from_user.username} in offtopic chat. {str(os.getenv('URL_OFFTOP'))}"
    bot_message = await bot.send_message(message.chat.id, msg)

    await asyncio.sleep(10)
    await bot.delete_message(message.chat.id, bot_message.message_id)


@dp.message_handler(filters.Command(['kick']), filters.AdminFilter())
async def listen_kick(message: types.Message):
    msg = f"@{message.reply_to_message.from_user.username} has been kicked {message.from_user.username}"

    await bot.send_message(message.chat.id, msg)
    await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)


@dp.message_handler(filters.Command(['kick']), filters.AdminFilter())
async def listen_ban(message: types.Message):
    msg = f"@{message.reply_to_message.from_user.username} has been banned {message.from_user.username}"

    await bot.send_message(message.chat.id, msg)
    await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)


if __name__ == '__main__':
    executor.start_polling(dp)
