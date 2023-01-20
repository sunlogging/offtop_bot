import asyncio
from datetime import datetime, timedelta

from aiogram import types
from aiogram.utils.markdown import hlink

from _module.command import text
from _module.tools import is_reply
from database.Manager import updata_info, is_warning, get_users


async def start(bot, message: types.Message):
    message_ = await bot.send_message(message.chat.id, text.start)

    await asyncio.sleep(3)
    await bot.delete_message(message.chat.id, message_.message_id)
    await bot.delete_message(message.chat.id, message.chat.id)


async def help(bot, message: types.Message):
    await bot.send_message(message.chat.id, text.help)


async def warning(bot, message: types.Message):
    admins = await bot.get_chat_administrators(message.chat.id)
    if not is_reply(message):
        if message.from_user.id in admins:
            await bot.send_message(message.chat.id, text.not_reply)
        else:
            await bot.send_message(message.chat.id, text.warning_user(1))
        return

    updata_info(message.reply_to_message.from_user.id, 'warning += 1')
    if is_warning(message.reply_to_message.from_user.id):
        await kick(bot, message, message.reply_to_message.from_user.id)


async def kick(bot, message: types.Message, call: int = None):
    if not is_reply(message) and call is None:
        await bot.send_message(message.chat.id, text.not_reply)
        return
    else:
        kick_user = message.reply_to_message
        admin = [message.from_user.id, message.from_user.username]
        if call is not None:
            bot_info = await bot.get_me()
            admin = [bot_info.id, bot_info.username]
        await bot.send_message(message.chat.id, text.kick_user(
            hlink(f'{kick_user.from_user.username}', f'tg://user?id={kick_user.from_user.id}'),
            hlink(f'{admin[1]}', f'tg://user?id={[0]}')), parse_mode="HTML")
        await bot.kick_chat_member(message.chat.id, kick_user.from_user.id)
        updata_info(message.from_user.id, 'is_kick = True')


async def ban(bot, message: types.Message):
    if not is_reply(message):
        await bot.send_message(message.chat.id, text.not_reply)
        return
    await bot.send_message(message.chat.id, text.ban_user(message.reply_to_message.from_user.id, message.from_user.id))
    await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    updata_info(message.from_user.id, 'is_ban = True')


async def mute(bot, message: types.Message):
    if not is_reply(message):
        await bot.send_message(message.chat.id, text.not_reply)
        return
    if len(message.text.split(' ')) < 2:
        await bot.send_message(message.chat.id, text.few_arguments)
    else:
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_send_messages=False)
        print(message.text.split(" ")[1])
        updata_info(message.from_user.id,
                    f'mute = {datetime.now() + timedelta(minutes=int(message.text.split(" ")[1]))}')


async def all(bot, message: types.Message, msg: str = ''):
    for user in get_users():
        msg += hlink(f'{user.username}', f'tg://user?id={user.id_user}') + ' '
    await bot.send_message(message.chat.id, msg, parse_mode='HTML')


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
