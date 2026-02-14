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
    "Black Burn Nutella": 4,
    "Black Burn Pinacolada": 4,
    "Black Burn Shock Currant": 4,
    "Black Burn Raspberry Shock": 6,
    "Black Burn Cherry Shock": 6,
    "Black Burn Famous Apple": 5,
    "Black Burn Red Orange": 6,
    "Black Burn Kiwi Stonier": 7,
    "Black Burn Black Honey": 7,
    "Black Burn Grapefruit": 5,
    "Black Burn Brownie": 7,
    "Black Burn Pear Lemonade": 7,
    "Black Burn Almond Ice Cream": 5,
    "Black Burn After 8": 6,
    "Black Burn Apple Shock": 5,
    "Black Burn Raspberries": 5,
    "Black Burn Etalon Melon": 6,
    "Black Burn Lemon Sweets": 6,
    "Black Burn Bananini": 5,
    "Black Burn Something Tropical": 5,
    "Black Burn Haribon": 8,
    "Black Burn Банановое Суфле": 6,
    "Black Burn Тропический Сок": 2,
    "Black Burn Mirinda": 7,
    "Black Burn Burberry Shock": 7,
    "Black Burn Lime Shock": 7,

    # --- OVERDOSE ---
    "Overdose Currant Mead": 0,
    "Overdose Maraschino Cherry": 6,
    "Overdose Apple Juicy": 3,
    "Overdose Strawberry Kiwi": 7,
    "Overdose Coffee": 6,

    # --- MUST HAVE ---
    "Must Have Melonade": 7,
    "Must Have Choco Mint": 10,
    "Must Have Ice Cream": 7,
    "Must Have Apple Drops": 6,
    "Must Have Berry Mors": 6,
    "Must Have Rocketman": 8,
    "Must Have Ice Mint": 8,
    "Must Have Sour Berries": 6,
    "Must Have Cola": 0,
    "Must Have Banana Mama": 2,
    "Must Have Cheesecake": 5,
    "Must Have Strawberry": 7,
    "Must Have Mango Sling": 5,
    "Must Have Pineapple Rings": 7,
    "Must Have Cookie": 8,
    "Must Have Orange Team": 5,
    "Must Have Sour Tropic": 6,
    "Must Have Undercoal": 5,
    "Must Have Caribbean Rum": 7,
    "Must Have Candy Cow": 6,
    "Must Have Cream Soda": 6,
    "Must Have Blueberry": 6,
    "Must Have Watermelon": 7,
    "Must Have Raspberry": 6,
    "Must Have Lemon and Lime": 6,

    # --- DARKSIDE ---
    "Darkside Dark Icecream": 7,
    "Darkside Mango Lassi": 6,
    "Darkside Wild Berry": 5,
    "Darkside Honey Dust": 6,
    "Darkside Mohito Yota": 6,
    "Darkside Pinekiller": 5,
    "Darkside Cyber Kiwi": 6,
    "Darkside Liquidator": 4,
    "Darkside Pineapple Pulse": 7,

    # --- NUR ---
    "Nur Pinacolada": 7,

    # --- ДРУГИЕ БРЕНДЫ ---
    "Молодость Яблоко": 3,
    "Молодость Энергетик и Бузина": 0,
    "Brusko Яблочный Штрудель": 7,
    "Brusko Пина Колада": 4,
    "Sebero Coco Like": 5,
    "Sebero Sunny Honey": 3,
    "Sebero Strawberry": 5,
    "Sebero Black and White": 7,
    "Sebero Very Peri": 4,
    "Sebero Bilberry": 2,
    "Sebero Caramel Glass": 7,
    "Sebero Шипучка Яблоко": 4,
    "Sebero Шипучка Лимон": 6,
    "Starline Гранатовый Сок": 6,
    "Starline Клюква": 5,
    "Starline Сливочный Крем": 7,
    "Starline Кислые Мармеладки": 3,
    "Starline Киви Смузи": 4,
    "Starline Лимонная Шипучка": 4,
    "Starline Ванильная Кола": 5,
    "Хулиган Апельсиновый Шоколад": 7,
    "Наш Мультфрукт": 3,
    "Наш Вишневый Сок": 4,
    "Наш Торфяной Виски": 5,
    "Adaya Mango Tango Ice": 2,
    "Adaya Sheik Money": 7,
    "Adaya Blue Melon": 7,
    "Adaya Jungle Jungle": 6,
    "Adaya Cherry Banana Ice": 6,
    "Adaya Cola Cherry": 4,
    "Adaya Mixfruits": 5,
    "Adaya Mi Amor": 5,
    "Adaya Orange": 4,
    "Adaya Raspberry": 6,
    "Adaya Watermelon": 6,
    "Adaya Green Apple": 3,
    "Adaya Ice": 7,
    "Adaya Milk": 6,
    "Северный Фрутомания": 5,
    "Jent Dolce Mint": 10,
    "Jent Coca Choca": 8,
    "Jent Marco Polo": 7,
    "Trofimoffs Grapefruit": 5,
    "Trofimoffs Peach": 7,
    "Trofimoffs Krick": 7,
    "Trofimoffs Wild Strawberry": 6,
    "Trofimoffs Hukheberry": 6,
    "DEUS YUZU": 6,
    "DUFT Blueberry": 6,
    "DUFT Kiwi Smoothie": 6,
    "DUFT Melon": 6,
    "DUFT Cherry Juice": 7,
    "Satyr Margarita": 6,
    "Satyr Ice Tangerine": 4,
    "Satyr Blood": 0,
    "Satyr Go! Go!": 6,
    "Element Raspberry": 5,
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

