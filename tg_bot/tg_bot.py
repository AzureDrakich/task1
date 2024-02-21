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
from hashlib import md5
from string import ascii_letters, digits

symbols = ascii_letters + digits


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
    /sign_in <username> <password>
    /send_msg <username> <message>
"""
active_users = {}

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(HELP)

@dp.message(Command("start"))
async def command_start(message: Message):
    await message.answer("Hello world")

@dp.message(Command("get_users"))
async def get_users(message: Message):
    text=[]
    r = requests.get(url + "/person")
    data = r.text
    n=""
    for i in data[2:-2]:
        if i in symbols:
            n+=i
        else:
            text.append(n)
            n=""
    users = [i for i in text if i]
    print(users)
    await message.answer("List of users:\n")
    for user in users:
        await message.answer(user)

@dp.message(Command("create_user"))
async def create_user(message: Message):
    data = message.text.split()
    js_data = {
        "name": data[1],
        "password": data[2]
    }
    requests.post(url + "/person", json=js_data)
    await message.answer("Username %s created" % data[1])

@dp.message(Command("sign_in"))
async def sign_in(message: Message):
    data = message.text.split()
    b_password = data[2].encode("utf-8")
    print(data[1],data[2],md5(b_password).hexdigest())
    js_data = {
        "name": data[1],
        "password": md5(b_password).hexdigest()
    }
    result = requests.get(url+"/%s" % data[1])
    if result:
        active_users[data[1]] = message.from_user.id
        print(active_users)
        await message.answer("Signed in as %s" % data[1])
    else:
        await message.answer("Wrong username or password")

@dp.message(Command("send_msg"))
async def send_msg(message: Message):
    data = message.text.split()
    print(data)
    if message.from_user.id in active_users.values():
        js_data = {
            "sender_id": message.from_user.id,
            "receiver_id": active_users[data[1]],
            "msg": data[2]
        }
        requests.post(url + "/chat", json=js_data)
    else:
        await message.answer("Unknown user or try to sign_in")


async def main():
    session = AiohttpSession(api=TelegramAPIServer.from_base("http://localhost:8000/api/v1"))
    bot = aiogram.Bot(TOKEN)
    await dp.start_polling(bot,session=session)

asyncio.run(main())
