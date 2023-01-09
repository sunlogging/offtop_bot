import asyncio
import logging


from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor

import settings

logging.basicConfig(level=logging.INFO)

bot = Bot(token='5922609233:AAHUIFUZFgiMGjz9AaAm6fB8Q3s8fIhfLDU')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def command_main(message: types.Message):
    print(message.chat.id)

    bot_message = await bot.send_message(message.chat.id, 'Bot is active')

    await asyncio.sleep(3)

    await bot.delete_message(message.chat.id, bot_message.message_id)
    await bot.delete_message(message.chat.id, message.message_id)

from aiogram.dispatcher import filters
@dp.message_handler(commands=['of', 'ban', 'kick'], is_chat_admin=True)
@dp.message_handler(filters.Command(['of', 'ban', 'kick']), filters.AdminFilter())
async def listen(message: types.Message):
    if message.text == '/of':
        msg = f"Who sent offtopic: @{message.from_user.username} \nUser from: @{message.reply_to_message.from_user.username}\n" + message.reply_to_message.text
        await bot.send_message(settings.Config.ID_OFFTOP, msg)

        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_message(message.chat.id, message.reply_to_message.message_id)

        msg = f"@{message.reply_to_message.from_user.username}, Your message has been sent @{message.from_user.username} in offtopic chat. {settings.Config.URL_OFFTOP}"
        bot_message = await bot.send_message(message.chat.id, msg)

        await asyncio.sleep(10)
        await bot.delete_message(message.chat.id, bot_message.message_id)

    elif message.text == '/kick':
        msg = f"@{message.reply_to_message.from_user.username} has been kicked {message.from_user.username}"

        await bot.send_message(message.chat.id, msg)
        await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)

    elif message.text == '/ban':
        msg = f"@{message.reply_to_message.from_user.username} has been banned {message.from_user.username}"

        await bot.send_message(message.chat.id, msg)
        await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)


if __name__ == '__main__':
    executor.start_polling(dp)
