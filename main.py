import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ---------- БАЗА ВКУСОВ ----------

flavors = {
    "Black Burn Overcola": 8,
    "Black Burn Ananas Shock": 9,
    "Black Burn Black Cola": 9,
    "Must Have Pinkman": 10,
    "Must Have Black Currant": 10,
    "Must Have Jumango": 9,
    "Must Have Sour Apple": 8,
    "Must Have Frosty": 10,
    "Darkside Cosmo Flower": 9,
    "Darkside Bana-Nascar": 8,
    "Overdose Baileys": 8,
    "Overdose Waffles": 8,
    "Banger Choko Mint": 8,
    "Jent Bachata": 10,
    "Jent Cigar": 10,
    "Nur Апельсин Черника": 8,
    "Adaya Angel Lips": 8,
    "Adaya Pinkman": 8,
    "Satyr Apelmizo": 7,
    "DUFT Watermelon": 7,
}

# ---------- ВЕСОВОЙ ПУЛ ----------

def build_weighted_pool():
    pool = []

    for name, rating in flavors.items():
        if rating >= 8:
            weight = 5
        elif rating >= 6:
            weight = 3
        elif rating >= 5:
            weight = 1
        else:
            weight = 0

        pool.extend([name] * weight)

    return pool


def generate_mix():
    pool = build_weighted_pool()

    unique_flavors = list(set(pool))

    if len(unique_flavors) < 3:
        random.shuffle(unique_flavors)
        return unique_flavors[0], unique_flavors[1], unique_flavors[2]

    first = random.choice(pool)
    pool = [f for f in pool if f != first]

    second = random.choice(pool)
    pool = [f for f in pool if f != second]

    third = random.choice(pool)

    return first, second, third

# ---------- FSM ----------

class MixForm(StatesGroup):
    choosing_base = State()
    choosing_taste = State()
    choosing_fresh = State()

bases = ["Десертный", "Фруктово-ягодный", "Гастрономия", "Тропический", "Напиток", "Цитрусовый"]

def base_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=b)] for b in bases],
        resize_keyboard=True
    )

taste_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сладкий")],
        [KeyboardButton(text="Кислый")]
    ],
    resize_keyboard=True
)

fresh_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Свежий")],
        [KeyboardButton(text="Нет")]
    ],
    resize_keyboard=True
)

regen_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Сгенерировать заново")]
    ],
    resize_keyboard=True
)

# ---------- ХЕНДЛЕРЫ ----------

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(MixForm.choosing_base)
    await message.answer("Какую основу выбираем?", reply_markup=base_keyboard())

@dp.message(MixForm.choosing_base)
async def choose_base(message: types.Message, state: FSMContext):
    await state.set_state(MixForm.choosing_taste)
    await message.answer("Характер вкуса?", reply_markup=taste_keyboard)

@dp.message(MixForm.choosing_taste)
async def choose_taste(message: types.Message, state: FSMContext):
    await state.set_state(MixForm.choosing_fresh)
    await message.answer("Добавить свежесть?", reply_markup=fresh_keyboard)

@dp.message(MixForm.choosing_fresh)
async def choose_fresh(message: types.Message, state: FSMContext):
    first, second, third = generate_mix()

    text = (
        "🔥 Твой микс:\n"
        f"60% {first}\n"
        f"30% {second}\n"
        f"10% {third}"
    )

    await message.answer(text, reply_markup=regen_keyboard)
    await state.clear()

@dp.message(lambda m: m.text == "🔄 Сгенерировать заново")
async def regenerate(message: types.Message):
    first, second, third = generate_mix()

    text = (
        "🔥 Новый микс:\n"
        f"60% {first}\n"
        f"30% {second}\n"
        f"10% {third}"
    )

    await message.answer(text, reply_markup=regen_keyboard)

# ---------- ЗАПУСК ----------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
