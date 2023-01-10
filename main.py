import logging
from typing import Optional

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import filters
from aiogram.utils import executor

import settings

logging.basicConfig(level=logging.INFO)

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot)


def is_reply(message) -> bool:
    if message.is_topic_message:
        return message.reply_to_message and \
               message.reply_to_message.message_id != message.message_thread_id

    return message.reply_to_message is not None


def get_thread_id(message) -> Optional[int]:
    return message.message_thread_id if message.is_topic_message else None


@dp.message_handler(filters.Command(['get_chat_id']))
async def get_chat_id(message: types.Message):
    if thread_id := get_thread_id(message):
        await message.reply(f'Chat id: {message.chat.id} thread_id: {thread_id}')
    else:
        await message.reply(f'Chat id {message.chat.id}')


@dp.message_handler(filters.Command(['of']), filters.AdminFilter())
async def listen_of(message: types.Message):
    if is_reply(message):
        await bot.forward_message(settings.OFF_TOP_CHAT_ID,
                                  message.chat.id,
                                  message.reply_to_message.message_id)

        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_message(message.chat.id, message.reply_to_message.message_id)


@dp.message_handler(filters.Command(['kick']), filters.AdminFilter())
async def listen_kick(message: types.Message):
    msg = f"@{message.reply_to_message.from_user.username} " \
          f"has been kicked {message.from_user.username}"

    await bot.send_message(message.chat.id, msg)
    await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)


@dp.message_handler(filters.Command(['ban']), filters.AdminFilter())
async def listen_ban(message: types.Message):
    msg = f"@{message.reply_to_message.from_user.username} " \
          f"has been banned {message.from_user.username}"

    await bot.send_message(message.chat.id, msg)
    await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)


if __name__ == '__main__':
    executor.start_polling(dp)
