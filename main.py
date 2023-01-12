import asyncio
import logging
from typing import Optional

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import filters
from aiogram.utils import executor

# webhook
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import Tests
import settings
from DatabaseManager import get_statistic, clear_statistic_table, search_id, add_user, update_count

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
    await Tests.database_test()
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


# stat


def check_permission_for_stat(func):
    async def check(message):
        if settings.STATISTICS:
            await func(message)
        else:
            pass

    return check


# TODO create content types = ALL
@dp.message_handler(filters.Command(commands='get', prefixes='!'))
@check_permission_for_stat
async def stat_listen_get(message: types.Message):
    stat = await get_statistic()
    msg = ""

    try:
        for index_top, user in enumerate(stat):
            if index_top == 0:
                msg += f"🥇 <i>{user[2]}</i> @{user[0]}\n"
            elif index_top == 1:
                msg += f"🥈 <i>{user[2]}</i> @{user[0]}\n"
            elif index_top == 2:
                msg += f"🥉 <i>{user[2]}</i> @{user[0]}\n"
            else:
                msg += f" {index_top + 1}. <i>{user[2]}</i> @{user[0]}\n"

        msg += f"\n@{stat[0][0]} <b>Wrote the most messages.</b> {stat[0][2]}\n\n"
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


@dp.message_handler(content_types=['text'])
@check_permission_for_stat
async def add_to_stat(message: types.Message):
    ids = await search_id(message.from_user.id)
    if not ids:
        await add_user(message.from_user.username, message.from_user.id)
        return
    await update_count(message.from_user.id)


if __name__ == '__main__':
    if settings.WEBHOOK:
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
