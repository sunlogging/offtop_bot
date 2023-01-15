import asyncio
import logging
from typing import Optional

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import filters
from aiogram.types import InputFile
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook
from aiogram.utils.markdown import hlink

import settings
import tools
from database_manager import get_statistic, clear_statistic_table, search_id, add_user, update_count, update_hour_count
from gen_schedule import create_schedule_last_hour
from tools import get_note_for_user

logging.basicConfig(level=logging.INFO)
bot = Bot(settings.BOT_TOKEN)
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


def get_thread_id(message) -> Optional[int]:
    return message.message_thread_id if message.is_topic_message else None


# debug
@dp.message_handler(filters.Command(['get_chat_id']))
async def get_chat_id(message: types.Message):
    if thread_id := get_thread_id(message):
        await message.reply(f'Chat id: {message.chat.id} thread_id: {thread_id}')
    else:
        await message.reply(f'Chat id {message.chat.id}')


# command
@dp.message_handler(commands=['start'])
async def command_main(message: types.Message):

    bot_message = await bot.send_message(message.chat.id,
                                         'Bot is active')

    await asyncio.sleep(3)

    await bot.delete_message(message.chat.id, bot_message.message_id)
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(filters.Command(['of']), filters.AdminFilter())
async def listen_of(message: types.Message):
    if not is_reply(message):
        await send_not_citation(message)
        return

    msg = \
        f"@{message.reply_to_message.from_user.username} Your message was @{message.from_user.username} " \
        f"sent offtopic. {settings.OFF_TOP_CHAT_URL}?"

    await bot.send_message(message.chat.id,
                           msg)

    await bot.forward_message(settings.OFF_TOP_CHAT_ID,
                              message.chat.id,
                              message.reply_to_message.message_id)

    await bot.delete_message(message.chat.id, message.message_id)
    await bot.delete_message(message.chat.id, message.reply_to_message.message_id)


@dp.message_handler(filters.Command(['kick']), filters.AdminFilter())
async def listen_kick(message: types.Message):
    if not is_reply(message):
        await send_not_citation(message)
        return

    msg = f"@{message.reply_to_message.from_user.username} " \
          f"has been kicked @{message.from_user.username}"

    await bot.send_message(message.chat.id, msg)
    await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)


@dp.message_handler(filters.Command(['ban']), filters.AdminFilter())
async def listen_ban(message: types.Message):
    if not is_reply(message):
        await send_not_citation(message)
        return

    msg = f"@{message.reply_to_message.from_user.username} " \
          f"has been banned @{message.from_user.username}"

    await bot.send_message(message.chat.id, msg)
    await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)


# webhook
async def on_startup(dp):
    await bot.set_webhook(settings.WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


def check_permission_for_stat(func):
    async def check(message):
        if settings.USE_STATISTICS:
            await func(message)
        else:
            pass

    return check



@dp.message_handler(filters.Command('all', prefixes='!'), filters.AdminFilter())
async def listen_all_command(message: types.Message):
    stat = await get_statistic()
    msg = ''
    try:
        for user in stat:
            msg += hlink(f"@{user[0]}", f'tg://user?id={user[1]}') + "\n"
        a = await bot.send_message(message.chat.id,
                                msg, parse_mode="HTML")

        """await asyncio.sleep(5)

        await bot.edit_message_text('@all',message.chat.id, a.message_id)"""
    except IndexError:
        msg = "Statistics is empty"
        await bot.send_message(message.chat.id,
                               msg,
                               parse_mode="HTML")


# TODO create content types = ALL
@dp.message_handler(filters.Command(commands='get', prefixes='!'))
@check_permission_for_stat
async def stat_listen_get(message: types.Message):
    stat = await get_statistic(message.chat.id)
    msg = ""

    try:
        for index_top, user in enumerate(stat):
            if index_top == 0:
                msg += f"🥇 <i>{user[-1]}</i> {get_note_for_user()}{user[0]}\n"
            elif index_top == 1:
                msg += f"🥈 <i>{user[-1]}</i> {get_note_for_user()}{user[0]}\n"
            elif index_top == 2:
                msg += f"🥉 <i>{user[-1]}</i> {get_note_for_user()}{user[0]}\n"
            else:
                msg += f" {index_top + 1}. <i>{user[-1]}</i> {get_note_for_user()}{user[0]}\n"

        msg += f"\n{stat[0][0]} <b>Wrote the most messages.</b> {stat[0][2]}\n\n"
        await create_schedule_last_hour()

        await bot.send_document(chat_id=message.chat.id, document=InputFile('active_last_hours.html'))
        await bot.send_message(message.chat.id,
                               msg,
                               parse_mode="HTML")
    except IndexError:
        msg = "Statistics is empty"
        await bot.send_message(message.chat.id,
                               msg,
                               parse_mode="HTML")


@dp.message_handler(filters.Command(commands='clear', prefixes='!'), filters.AdminFilter())
@check_permission_for_stat
async def stat_listen_clear(message: types.Message):
    await clear_statistic_table()

    msg = "<b>Stats have been reset!</b>"
    await bot.send_message(message.chat.id,
                           msg,
                           parse_mode="HTML")




# TODO media
@dp.message_handler(content_types=[])
@check_permission_for_stat
async def add_to_stat(message: types.Message):
    print(1)
    ids = await search_id(message.from_user.id)
    if not ids:
        await add_user(message.from_user.username, message.from_user.id, message.chat.id)

        return
    if '!all' in message.text.split(' '):

        await listen_all_command(message)

    await update_count(message.from_user.id)
    await update_hour_count(message.date.hour)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tools.database_test())

    if settings.USE_WEBHOOK:
        dp.middleware.setup(LoggingMiddleware())

        start_webhook(
            dispatcher=dp,
            webhook_path=settings.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=settings.WEBAPP_HOST,
            port=settings.WEBAPP_PORT,
        )
    else:
        executor.start_polling(dp, skip_updates=True)
