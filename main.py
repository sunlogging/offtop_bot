import asyncio
import logging

from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import filters

from settings import ID_OFFTOP, URL_OFFTOP, TOKEN

logging.basicConfig(level=logging.INFO)


bot = Bot(TOKEN)
dp = Dispatcher(bot)

def is_reply(message: types.Message) -> bool:
    if message.is_topic_message:
        return message.reply_to_message and \
               message.reply_to_message.message_id != message.message_thread_id

    return message.reply_to_message is not None

async def send_not_citation(message: types.Message):
    msg = "There is no citation for the post"
    bot_message = await bot.send_message(message.chat.id, msg)

    await asyncio.sleep(10)
    await bot.delete_message(message.chat.id, bot_message.message_id)
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(commands=['start'])
async def command_main(message: types.Message):
    print(message.chat.username,message.chat.id)

    bot_message = await bot.send_message(message.chat.id, 'Bot is active')

    await asyncio.sleep(3)

    await bot.delete_message(message.chat.id, bot_message.message_id)
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(filters.Command(['of']), filters.AdminFilter())
async def listen_of(message: types.Message):

    #msg = f"Who sent offtopic: @{message.from_user.username}"
    #await bot.send_message(ID_OFFTOP, msg)

    if not is_reply(message):
        await send_not_citation(message)
        return
    await bot.forward_message(ID_OFFTOP, message.chat.id, message.reply_to_message.message_id)

    await bot.delete_message(message.chat.id, message.message_id)

    await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    msg = f"@{message.reply_to_message.from_user.username}, Your message has been sent @{message.from_user.username} in offtopic chat. {URL_OFFTOP}"
    await bot.send_message(message.chat.id, msg)

    #await asyncio.sleep(10)
    #await bot.delete_message(message.chat.id, bot_message.message_id)


@dp.message_handler(filters.Command(['kick']), filters.AdminFilter())
async def listen_kick(message: types.Message):
    if not is_reply(message):
        await send_not_citation(message)
        return

    msg = f"@{message.reply_to_message.from_user.username} has been kicked {message.from_user.username}"

    await bot.send_message(message.chat.id, msg)
    await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)


@dp.message_handler(filters.Command(['ban']), filters.AdminFilter())
async def listen_ban(message: types.Message):
    if not is_reply(message):
        await send_not_citation(message)
        return

    msg = f"@{message.reply_to_message.from_user.username} has been banned {message.from_user.username}"

    await bot.send_message(message.chat.id, msg)
    await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)


if __name__ == '__main__':
    executor.start_polling(dp)
