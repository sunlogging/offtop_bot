import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import filters
from aiogram.utils import executor
from aiogram.utils.markdown import hlink

import _module.text as text
from _module.tools import is_reply
from database.Manager import add_user, get_user, updata_info, is_warning, get_users

logging.basicConfig(level=logging.INFO)

bot = ""
dp = ""

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


def start_bot(config: dict):
    bot = Bot(config.get('TOKEN'))
    dp = Dispatcher(bot)

    @dp.message_handler(commands='start')
    async def listen_command_start(message: types.Message):
        message_ = await bot.send_message(message.chat.id, text.start)

        await asyncio.sleep(3)
        await bot.delete_message(message.chat.id, message_.message_id)
        await bot.delete_message(message.chat.id, message.message_id)

    @dp.message_handler(filters.Command(['help']))
    async def listen_command_help(message: types.Message):
        await bot.send_message(message.chat.id, text.help)

    @dp.message_handler(filters.Command(['warning']))
    async def listen_command_warning(message: types.Message):
        admins = await bot.get_chat_administrators(message.chat.id)
        if not is_reply(message):
            if message.from_user.id in admins:
                await bot.send_message(message.chat.id, text.not_reply)
            else:
                await bot.send_message(message.chat.id, text.warning_user(1))
            return

        updata_info(message.reply_to_message.from_user.id, 'warning += 1')
        if is_warning(message.reply_to_message.from_user.id):
            await listen_command_kick(bot, message, message.reply_to_message.from_user.id)

    @dp.message_handler(filters.Command(['kick']))
    async def listen_command_kick(message: types.Message, call=None):
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

    @dp.message_handler(filters.Command(['ban']))
    async def listen_command_ban(message: types.Message):
        if not is_reply(message):
            await bot.send_message(message.chat.id, text.not_reply)
            return
        await bot.send_message(message.chat.id,
                               text.ban_user(message.reply_to_message.from_user.id, message.from_user.id))
        await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        updata_info(message.from_user.id, 'is_ban = True')

    @dp.message_handler(filters.Command(['mute']))
    async def listen_command_mute(message: types.Message):
        if not is_reply(message):
            await bot.send_message(message.chat.id, text.not_reply)
            return
        if len(message.text.split(' ')) < 2:
            await bot.send_message(message.chat.id, text.few_arguments)
        else:
            await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                           can_send_messages=False)
            print(message.text.split(" ")[1])
            updata_info(message.from_user.id,
                        f'mute = {datetime.now() + timedelta(minutes=int(message.text.split(" ")[1]))}')

    @dp.message_handler(filters.Command(['all']))
    async def all(bot, message: types.Message, msg: str = ''):
        for user in get_users():
            msg += hlink(f'{user.username}', f'tg://user?id={user.id_user}') + ' '
        await bot.send_message(message.chat.id, msg, parse_mode='HTML')

    @dp.message_handler(filters.Command(['of', 'top']))
    async def listen_command_of(message: types.Message):
        if message.text == '/of':
            await of_top(bot, message, config.get('CHAT_URL_OFFTOPIC'), config.get('CHAT_ID_OFFTOPIC'))
        elif message.text == '/top':
            await of_top(bot, message, config.get('CHAT_URL_MAIN'), config.get('CHAT_ID_MAIN'))

    @dp.message_handler(filters.Command(['stat_group'], prefixes='!'))
    async def listen_command_stat_group(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['stat_users'], prefixes='!'))
    async def listen_command_stat_users(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['stat_user'], prefixes='!'))
    async def listen_command_stat_user(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['stat_rules'], prefixes='!'))
    async def listen_command_stat_rules(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['stat_isbot'], prefixes='!'))
    async def listen_command_stat_isbot(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['stat_isspam'], prefixes='!'))
    async def listen_command_stat_isspam(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['check_file'], prefixes='&'))
    async def listen_command_check_file(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['check_link'], prefixes='&'))
    async def listen_command_check_link(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['check_lang'], prefixes='&'))
    async def listen_command_check_lang(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['interpreter'], prefixes='&'))
    async def listen_command_interpreter(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['translator'], prefixes='&'))
    async def listen_command_translator(message: types.Message):
        ...

    def get_thread_id(message):
        return message.message_thread_id if message.is_topic_message else None

    # debug
    @dp.message_handler(filters.Command(['get_chat_id']))
    async def get_chat_id(message: types.Message):
        if thread_id := get_thread_id(message):
            await message.reply(f'Chat id: {message.chat.id} thread_id: {thread_id}')
        else:
            await message.reply(f'Chat id {message.chat.id}')

    @dp.message_handler(content_types=["new_chat_members"])
    async def on_user_joined(message: types.Message):
        await message.delete()
        group_info = await bot.get_chat(message.chat.id)
        msg = group_info.bio \
              + '\n\n\nBefore we allow you to chat, please do a little check to see if you are human.'
        await bot.send_message(message.chat.id, msg)
        updata_info(message.from_user.id, 'is_bot = True')

    @dp.message_handler(content_types=["text"])
    async def listen_all_message(message: types.Message):
        if get_user(message.from_user.id) is None:
            add_user(message.from_user.id, message.from_user.username)
        else:
            updata_info(message.from_user.id, 'messages += 1')


    #dp.regist_message_handler(listen_bot_check_button, types.Message)

    executor.start_polling(dp, skip_updates=True, timeout=200)

