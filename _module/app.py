import logging


from aiogram import Dispatcher, Bot
from aiogram.dispatcher import filters
from aiogram.utils import executor

from _module.command_classic.command import *

logging.basicConfig(level=logging.INFO)

bot = ""
dp = ""

def start_bot(config: dict):
    bot = Bot(config.get('TOKEN'))
    dp = Dispatcher(bot)


    @dp.message_handler(commands='start')
    async def listen_command_start(message: types.Message):
        await start(bot, message)

    @dp.message_handler(filters.Command(['help']))
    async def listen_command_help(message: types.Message):
        await help(bot, message)

    @dp.message_handler(filters.Command(['warning']))
    async def listen_command_warning(message: types.Message):
        await warning(bot, message)

    @dp.message_handler(filters.Command(['kick']))
    async def listen_command_kick(message: types.Message):
        await kick(bot, message)

    @dp.message_handler(filters.Command(['ban']))
    async def listen_command_ban(message: types.Message):
        await ban(bot, message)

    @dp.message_handler(filters.Command(['mute']))
    async def listen_command_mute(message: types.Message):
        ...

    @dp.message_handler(filters.Command(['all']))
    async def listen_command_all(message: types.Message):
        ...

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

    executor.start_polling(dp, skip_updates=True)
