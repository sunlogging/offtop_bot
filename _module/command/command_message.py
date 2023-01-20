import aiohttp
from aiogram import types


async def listen_command_check_file(bot, message: types.Message):
    ...



async def listen_command_check_link(bot, message: types.Message, key):
    # async with aiohttp.ClientSession() as session:
    #     for url in urls:
    #         params = {'apikey': key, 'resource': url}
    #         async with session.get('https://www.virustotal.com/vtapi/v2/file/report', params=params) as response:
    #             print("Status:", response.status)
    #             print("Content-type:", response.headers['content-type'])
    #
    #             html = await response.text()
    #             print("Body:", html)
    ...



async def listen_command_check_lang(bot, message: types.Message):
    ...



async def listen_command_interpreter(bot, message: types.Message):
    ...



async def listen_command_translator(bot, message: types.Message):
    ...
