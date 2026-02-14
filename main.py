import asyncio
import os
import random
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

FILE = "ratings.json"

# ---------- БАЗА ----------

dessert = {
    "brownie": 7,
    "ice cream": 7,
    "cookie": 7.5,
    "waffles": 8
}

fruit = {
    "pinkman": 10,
    "black currant": 10,
    "raspberry": 6,
    "watermelon": 7
}

sour = {
    "lime shock": 7,
    "lemon": 6,
    "sour apple": 8
}

fresh = {
    "mint": 8,
    "frosty": 10
}

# ---------- ЗАГРУЗКА ----------

def load():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

likes = load()
last_mix = []

# ---------- ВЫБОР ----------

def pick(category):
    weighted = []
    for name, rating in category.items():
        bonus = likes.get(name, 0)
        weight = max(1, int(rating + bonus))
        weighted += [name] * weight
    return random.choice(weighted)

def make_mix():
    global last_mix
    last_mix = [
        pick(fruit),
        pick(sour),
        pick(fresh)
    ]
    return last_mix

# ---------- КНОПКИ ----------

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👍"), KeyboardButton(text="👎")]
    ],
    resize_keyboard=True
)

# ---------- ХЕНДЛЕРЫ ----------

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer("Напиши /mix для генерации")

@dp.message(Command("mix"))
async def mix(msg: types.Message):
    mix_data = make_mix()

    text = (
        "🔥 Микс:\n"
        f"60% {mix_data[0]}\n"
        f"30% {mix_data[1]}\n"
        f"10% {mix_data[2]}"
    )

    await msg.answer(text, reply_markup=kb)

@dp.message(lambda m: m.text in ["👍", "👎"])
async def rate(msg: types.Message):
    change = 1 if msg.text == "👍" else -1

    for flavor in last_mix:
        likes[flavor] = likes.get(flavor, 0) + change

    save(likes)

    await msg.answer("Запомнил 👍")

# ---------- ЗАПУСК ----------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
