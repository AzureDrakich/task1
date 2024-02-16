import aiogram
import asyncio
import requests
import json
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.handlers import MessageHandler
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

with open("token") as f:
    token = f.read()
url = "http://localhost:8000/api/v1"
TOKEN = token
dp = aiogram.Dispatcher()
router = Router()
HELP = """/help
    /start
    /get_users
    /create_user <username> <password>
"""

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(HELP)
@dp.message(Command("start"))
async def command_start(message: Message):
    await message.answer("Hello world")

@dp.message(Command("get_users"))
async def get_users(message: Message):
    r = requests.get(url + "/person")
    data = r.text
    await message.answer(data)
@dp.message(Command("create_user"))
async def create_user(message: Message):
    data = message.text.split()
    js_data = {
        "name": data[1],
        "password": data[2]
    }
    requests.post(url + "/person", json=js_data)
    await message.answer("Username %s created" % data[1])


async def main():
    session = AiohttpSession(api=TelegramAPIServer.from_base("http://localhost:8000/api/v1"))
    bot = aiogram.Bot(TOKEN)
    await dp.start_polling(bot,session=session)

asyncio.run(main())
