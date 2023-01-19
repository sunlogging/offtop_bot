import asyncio

from aiogram import types

from _module.command_classic import text
from _module.tools import is_reply
from database.Manager import updata_info, is_warning


async def start(bot, message: types.Message):
    message_ = await bot.send_message(message.chat.id, text.start)

    await asyncio.sleep(3)
    await bot.delete_message(message.chat.id, message_.message_id)

async def help(bot, message: types.Message):
    await bot.send_message(message.chat.id, text.help)


async def warning(bot, message: types.Message):
    admins = bot.get_chat_administrators()
    if not is_reply(message):
        if message.from_user.id in admins:
            await bot.send_message(message.chat.id, text.not_reply)
        else:
            await bot.send_message(message.chat.id, text.warning_user(1))
        return

    updata_info(message.reply_to_message.from_user.id, 'warning += 1')
    if is_warning(message.reply_to_message.from_user.id):
        await kick(bot, message, message.reply_to_message.from_user.id)

async def kick(bot, message: types.Message, call: int=None):
    if not is_reply(message) and call is None:
        await bot.send_message(message.chat.id, text.not_reply)
        return
    else:
        kick_user = message.reply_to_message.from_user.id
        admin = message.from_user.id
        if call is not None:
            kick_user = call
            admin = await bot.get_me()
            print(admin)
        await bot.send_message(message.chat.id, text.kick_user(kick_user, admin))
        await bot.kick_chat_member(message.chat.id, kick_user)
        updata_info(message.from_user.id, 'is_kick = True')

async def ban(bot, message: types.Message):
    if not is_reply(message):
        await bot.send_message(message.chat.id, text.not_reply)
        return
    await bot.send_message(message.chat.id, text.ban_user(message.reply_to_message.from_user.id, message.from_user.id))
    await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    updata_info(message.from_user.id, 'is_ban = True')

async def mute(bot, message: types.Message):
    ...

async def all(bot, message: types.Message):
    ...

async def of_top(bot, message: types.Message, chat_url: str, chat_id: int):
    if not is_reply(message):
        await bot.send_message(message.chat.id, text.not_reply)
        return

    msg = \
        f"@{message.reply_to_message.from_user.username} Your message was @{message.from_user.username} " \
        f"sent offtopic. {chat_url}?"

    await bot.send_message(message.chat.id,
                           msg)

    await bot.forward_message(chat_id,
                              message.chat.id,
                              message.reply_to_message.message_id)

    await bot.delete_message(message.chat.id, message.message_id)
    await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
