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

# ================== БАЗА ВКУСОВ ==================

flavors = {

    "Десертный": {
        "Black Burn Nutella": 4,
        "Black Burn Brownie": 7,
        "Black Burn Almond Ice Cream": 5,
        "Black Burn After 8": 6,
        "Must Have Cheesecake": 5,
        "Must Have Cookie": 8,
        "Must Have Ice Cream": 7,
        "Must Have Candy Cow": 6,
        "Overdose Waffles": 8,
        "Overdose Baileys": 8,
        "Overdose Coffee": 6,
        "Starline Сливочный Крем": 7,
        "Sebero Caramel Glass": 7,
        "Sebero Black and White": 7,
        "Brusko Яблочный Штрудель": 7,
        "Хулиган Апельсиновый Шоколад": 7,
        "Adaya Milk": 6,
        "Must Have Choco Mint": 10,
        "Banger Choko Mint": 8,
        "Jent Dolce Mint": 10,
    },

    "Фруктово-ягодный": {
        "Must Have Pinkman": 10,
        "Must Have Black Currant": 10,
        "Must Have Berry Mors": 6,
        "Must Have Strawberry": 7,
        "Must Have Raspberry": 6,
        "Must Have Blueberry": 6,
        "Must Have Watermelon": 7,
        "DUFT Watermelon": 7,
        "DUFT Cherry Juice": 7,
        "DUFT Blueberry": 6,
        "Element Raspberry": 5,
        "Trofimoffs Wild Strawberry": 6,
        "Trofimoffs Krick": 7,
        "Trofimoffs Hukheberry": 6,
        "Starline Клюква": 5,
        "Starline Гранатовый Сок": 6,
        "Adaya Pinkman": 8,
        "Adaya Raspberry": 6,
        "Adaya Watermelon": 6,
        "Adaya Blue Melon": 7,
        "Sebero Strawberry": 5,
        "Sebero Bilberry": 2,
        "Наш Вишневый Сок": 4,
        "Северный Фрутомания": 5,
    },

    "Цитрусовый": {
        "Black Burn Red Orange": 6,
        "Black Burn Lime Shock": 7,
        "Black Burn Grapefruit": 5,
        "Black Burn Lemon Sweets": 6,
        "Must Have Lemon and Lime": 6,
        "Must Have Sour Apple": 8,
        "Satyr Ice Tangerine": 4,
        "Satyr Margarita": 6,
        "DEUS YUZU": 6,
        "Trofimoffs Grapefruit": 5,
        "Sebero Шипучка Лимон": 6,
        "Starline Лимонная Шипучка": 4,
        "Adaya Orange": 4,
    },

    "Тропический": {
        "Black Burn Ananas Shock": 9,
        "Black Burn Pinacolada": 4,
        "Black Burn Something Tropical": 5,
        "Black Burn Тропический Сок": 2,
        "Must Have Jumango": 9,
        "Must Have Mango Sling": 5,
        "Must Have Pineapple Rings": 7,
        "Must Have Sour Tropic": 6,
        "Nur Pinacolada": 7,
        "Darkside Pineapple Pulse": 7,
        "Darkside Mango Lassi": 6,
        "Overdose Strawberry Kiwi": 7,
        "Adaya Mango Tango Ice": 2,
        "Adaya Jungle Jungle": 6,
        "Brusko Пина Колада": 4,
    },

    "Напиток": {
        "Black Burn Overcola": 8,
        "Black Burn Black Cola": 9,
        "Black Burn Mirinda": 7,
        "Must Have Cola": 0,
        "Must Have Cream Soda": 6,
        "Must Have Melonade": 7,
        "Must Have Rocketman": 8,
        "Starline Ванильная Кола": 5,
        "Adaya Cola Cherry": 4,
        "Darkside Mohito Yota": 6,
        "Overdose Currant Mead": 0,
        "Наш Торфяной Виски": 5,
        "Must Have Caribbean Rum": 7,
        "Jent Coca Choca": 8,
    },

    "Гастрономия": {
        "Jent Cigar": 10,
        "Darkside Honey Dust": 6,
        "Darkside Pinekiller": 5,
        "Darkside Dark Icecream": 7,
        "Black Burn Black Honey": 7,
        "Black Burn Haribon": 8,
        "Adaya Sheik Money": 7,
        "Adaya Mi Amor": 5,
        "Sebero Sunny Honey": 3,
    },

    "Свежесть": {
        "Must Have Frosty": 10,
        "Must Have Ice Mint": 8,
        "Adaya Ice": 7,
    }
}

# ================== FSM ==================

class MixForm(StatesGroup):
    choosing_base = State()
    choosing_taste = State()
    choosing_fresh = State()

bases = list(flavors.keys())
bases.remove("Свежесть")

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

# ================== ЛОГИКА ВЫБОРА ==================

def build_weighted_pool(category_dict, exclude=None):
    pool = []

    for name, rating in category_dict.items():
        if exclude and name in exclude:
            continue

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


def generate_mix(base_category, fresh_choice):

    # 60%
    base_pool = build_weighted_pool(flavors[base_category])
    first = random.choice(base_pool)

    # 30%
    all_flavors = {}
    for cat, items in flavors.items():
        if cat != "Свежесть":
            all_flavors.update(items)

    second_pool = build_weighted_pool(all_flavors, exclude=[first])
    second = random.choice(second_pool)

    # 10%
    if fresh_choice == "Свежий":
        third_pool = build_weighted_pool(flavors["Свежесть"], exclude=[first, second])
    else:
        third_pool = build_weighted_pool(all_flavors, exclude=[first, second])

    third = random.choice(third_pool)

    return first, second, third

# ================== ХЕНДЛЕРЫ ==================

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(MixForm.choosing_base)
    await message.answer("Какую основу выбираем?", reply_markup=base_keyboard())

@dp.message(MixForm.choosing_base)
async def choose_base(message: types.Message, state: FSMContext):
    await state.update_data(base=message.text)
    await state.set_state(MixForm.choosing_taste)
    await message.answer("Характер вкуса?", reply_markup=taste_keyboard)

@dp.message(MixForm.choosing_taste)
async def choose_taste(message: types.Message, state: FSMContext):
    await state.set_state(MixForm.choosing_fresh)
    await message.answer("Добавить свежесть?", reply_markup=fresh_keyboard)

@dp.message(MixForm.choosing_fresh)
async def choose_fresh(message: types.Message, state: FSMContext):

    data = await state.get_data()
    base = data["base"]

    first, second, third = generate_mix(base, message.text)

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
    first, second, third = generate_mix("Фруктово-ягодный", "Нет")

    text = (
        "🔥 Новый микс:\n"
        f"60% {first}\n"
        f"30% {second}\n"
        f"10% {third}"
    )

    await message.answer(text, reply_markup=regen_keyboard)

# ================== ЗАПУСК ==================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

