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
# формат: "Название": (рейтинг, профиль) где профиль: sweet | sour | neutral

flavors = {

    "Десертный": {
        "Black Burn Nutella": (4, "sweet"),
        "Black Burn Brownie": (7, "sweet"),
        "Black Burn Almond Ice Cream": (5, "sweet"),
        "Black Burn After 8": (6, "neutral"),
        "Must Have Cheesecake": (5, "sweet"),
        "Must Have Cookie": (8, "sweet"),
        "Must Have Ice Cream": (7, "sweet"),
        "Must Have Candy Cow": (6, "sweet"),
        "Overdose Waffles": (8, "sweet"),
        "Overdose Baileys": (8, "sweet"),
        "Overdose Coffee": (6, "neutral"),
        "Starline Сливочный Крем": (7, "sweet"),
        "Sebero Caramel Glass": (7, "sweet"),
        "Sebero Black and White": (7, "sweet"),
        "Brusko Яблочный Штрудель": (7, "sweet"),
        "Хулиган Апельсиновый Шоколад": (7, "sweet"),
        "Adaya Milk": (6, "sweet"),
        "Must Have Choco Mint": (10, "neutral"),
        "Banger Choko Mint": (8, "neutral"),
        "Jent Dolce Mint": (10, "neutral"),
    },

    "Фруктово-ягодный": {
        "Must Have Pinkman": (10, "sweet"),
        "Must Have Black Currant": (10, "sweet"),
        "Must Have Berry Mors": (6, "sweet"),
        "Must Have Strawberry": (7, "sweet"),
        "Must Have Raspberry": (6, "sweet"),
        "Must Have Blueberry": (6, "sweet"),
        "Must Have Watermelon": (7, "sweet"),
        "DUFT Watermelon": (7, "sweet"),
        "DUFT Cherry Juice": (7, "sweet"),
        "DUFT Blueberry": (6, "sweet"),
        "Element Raspberry": (5, "sweet"),
        "Trofimoffs Wild Strawberry": (6, "sweet"),
        "Trofimoffs Krick": (7, "sweet"),
        "Trofimoffs Hukheberry": (6, "sweet"),
        "Starline Клюква": (5, "sour"),
        "Starline Гранатовый Сок": (6, "sweet"),
        "Adaya Pinkman": (8, "sweet"),
        "Adaya Raspberry": (6, "sweet"),
        "Adaya Watermelon": (6, "sweet"),
        "Adaya Blue Melon": (7, "sweet"),
        "Sebero Strawberry": (5, "sweet"),
        "Sebero Bilberry": (2, "sweet"),
        "Наш Вишневый Сок": (4, "sweet"),
        "Северный Фрутомания": (5, "sweet"),
    },

    "Цитрусовый": {
        "Black Burn Red Orange": (6, "sour"),
        "Black Burn Lime Shock": (7, "sour"),
        "Black Burn Grapefruit": (5, "sour"),
        "Black Burn Lemon Sweets": (6, "sour"),
        "Must Have Lemon and Lime": (6, "sour"),
        "Must Have Sour Apple": (8, "sour"),
        "Satyr Ice Tangerine": (4, "sour"),
        "Satyr Margarita": (6, "sour"),
        "DEUS YUZU": (6, "sour"),
        "Trofimoffs Grapefruit": (5, "sour"),
        "Sebero Шипучка Лимон": (6, "sour"),
        "Starline Лимонная Шипучка": (4, "sour"),
        "Adaya Orange": (4, "sour"),
    },

    "Тропический": {
        "Black Burn Ananas Shock": (9, "sweet"),
        "Black Burn Pinacolada": (4, "sweet"),
        "Black Burn Something Tropical": (5, "sweet"),
        "Black Burn Тропический Сок": (2, "sweet"),
        "Must Have Jumango": (9, "sweet"),
        "Must Have Mango Sling": (5, "sweet"),
        "Must Have Pineapple Rings": (7, "sweet"),
        "Must Have Sour Tropic": (6, "sour"),
        "Nur Pinacolada": (7, "sweet"),
        "Darkside Pineapple Pulse": (7, "sweet"),
        "Darkside Mango Lassi": (6, "sweet"),
        "Overdose Strawberry Kiwi": (7, "sweet"),
        "Adaya Mango Tango Ice": (2, "sweet"),
        "Adaya Jungle Jungle": (6, "sweet"),
        "Brusko Пина Колада": (4, "sweet"),
    },

    "Напиток": {
        "Black Burn Overcola": (8, "sweet"),
        "Black Burn Black Cola": (9, "sweet"),
        "Black Burn Mirinda": (7, "sweet"),
        "Must Have Cola": (0, "sweet"),
        "Must Have Cream Soda": (6, "sweet"),
        "Must Have Melonade": (7, "sweet"),
        "Must Have Rocketman": (8, "sweet"),
        "Starline Ванильная Кола": (5, "sweet"),
        "Adaya Cola Cherry": (4, "sweet"),
        "Darkside Mohito Yota": (6, "sour"),
        "Overdose Currant Mead": (0, "sweet"),
        "Наш Торфяной Виски": (5, "neutral"),
        "Must Have Caribbean Rum": (7, "neutral"),
        "Jent Coca Choca": (8, "sweet"),
    },

    "Гастрономия": {
        "Jent Cigar": (10, "neutral"),
        "Darkside Honey Dust": (6, "sweet"),
        "Darkside Pinekiller": (5, "neutral"),
        "Darkside Dark Icecream": (7, "sweet"),
        "Black Burn Black Honey": (7, "sweet"),
        "Black Burn Haribon": (8, "sweet"),
        "Adaya Sheik Money": (7, "neutral"),
        "Adaya Mi Amor": (5, "sweet"),
        "Sebero Sunny Honey": (3, "sweet"),
    },

    "Свежесть": {
        "Must Have Frosty": (10, "neutral"),
        "Must Have Ice Mint": (8, "neutral"),
        "Adaya Ice": (7, "neutral"),
    }
}

# ================== FSM ==================

class MixForm(StatesGroup):
    choosing_base = State()
    choosing_taste = State()
    choosing_fresh = State()

# Запоминаем последний выбор пользователя:
# user_id -> (base, taste, fresh)
user_last_choice = {}

bases = [k for k in flavors.keys() if k != "Свежесть"]

def base_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=b)] for b in bases],
        resize_keyboard=True
    )

taste_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Сладкий")],
              [KeyboardButton(text="Кислый")]],
    resize_keyboard=True
)

fresh_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Свежий")],
              [KeyboardButton(text="Нет")]],
    resize_keyboard=True
)

# Клавиатура после выдачи микса
post_mix_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Сгенерировать заново")],
        [KeyboardButton(text="🆕 Новый кальян")]
    ],
    resize_keyboard=True
)

# ================== ЛОГИКА ВЫБОРА ==================

def build_weighted_pool(category_dict, taste, exclude=None):
    pool = []
    exclude = set(exclude or [])

    for name, (rating, profile) in category_dict.items():
        if name in exclude:
            continue

        # базовый вес по рейтингу
        if rating >= 8:
            weight = 5
        elif rating >= 6:
            weight = 3
        elif rating >= 5:
            weight = 1
        else:
            weight = 0

        # усиление по характеру вкуса
        if taste == "Сладкий" and profile == "sweet":
            weight *= 2
        elif taste == "Кислый" and profile == "sour":
            weight *= 2

        if weight > 0:
            pool.extend([name] * weight)

    return pool


def all_non_fresh_flavors():
    merged = {}
    for cat, items in flavors.items():
        if cat != "Свежесть":
            merged.update(items)
    return merged


def generate_mix(base_category, taste, fresh_choice):
    # 60% — из выбранной категории
    base_pool = build_weighted_pool(flavors[base_category], taste)
    if not base_pool:
        base_pool = list(flavors[base_category].keys())
    first = random.choice(base_pool)

    # 30% — из всех кроме свежести
    all_flavs = all_non_fresh_flavors()
    second_pool = build_weighted_pool(all_flavs, taste, exclude=[first])
    if not second_pool:
        second_pool = [k for k in all_flavs.keys() if k != first]
    second = random.choice(second_pool)

    # 10% — свежесть если выбрали "Свежий", иначе из всех кроме свежести
    if fresh_choice == "Свежий":
        third_pool = build_weighted_pool(flavors["Свежесть"], taste, exclude=[first, second])
        if not third_pool:
            third_pool = [k for k in flavors["Свежесть"].keys() if k not in {first, second}]
    else:
        third_pool = build_weighted_pool(all_flavs, taste, exclude=[first, second])
        if not third_pool:
            third_pool = [k for k in all_flavs.keys() if k not in {first, second}]

    third = random.choice(third_pool)

    return first, second, third

# ================== ХЕНДЛЕРЫ ==================

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(MixForm.choosing_base)
    await message.answer("Какую основу выбираем?", reply_markup=base_keyboard())

@dp.message(MixForm.choosing_base)
async def choose_base(message: types.Message, state: FSMContext):
    if message.text not in bases:
        await message.answer("Выбери основу кнопкой ниже 👇", reply_markup=base_keyboard())
        return

    await state.update_data(base=message.text)
    await state.set_state(MixForm.choosing_taste)
    await message.answer("Характер вкуса?", reply_markup=taste_keyboard)

@dp.message(MixForm.choosing_taste)
async def choose_taste(message: types.Message, state: FSMContext):
    if message.text not in ["Сладкий", "Кислый"]:
        await message.answer("Выбери вариант кнопкой ниже 👇", reply_markup=taste_keyboard)
        return

    await state.update_data(taste=message.text)
    await state.set_state(MixForm.choosing_fresh)
    await message.answer("Добавить свежесть?", reply_markup=fresh_keyboard)

@dp.message(MixForm.choosing_fresh)
async def choose_fresh(message: types.Message, state: FSMContext):
    if message.text not in ["Свежий", "Нет"]:
        await message.answer("Выбери вариант кнопкой ниже 👇", reply_markup=fresh_keyboard)
        return

    data = await state.get_data()
    base = data["base"]
    taste = data["taste"]
    fresh = message.text

    user_last_choice[message.from_user.id] = (base, taste, fresh)

    first, second, third = generate_mix(base, taste, fresh)

    text = f"🔥 Твой микс:\n60% {first}\n30% {second}\n10% {third}"
    await message.answer(text, reply_markup=post_mix_keyboard)
    await state.clear()

@dp.message(lambda m: m.text == "🔄 Сгенерировать заново")
async def regenerate(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_last_choice:
        await message.answer("Сначала создай микс через /start", reply_markup=base_keyboard())
        return

    base, taste, fresh = user_last_choice[user_id]
    first, second, third = generate_mix(base, taste, fresh)

    text = f"🔥 Новый микс:\n60% {first}\n30% {second}\n10% {third}"
    await message.answer(text, reply_markup=post_mix_keyboard)

@dp.message(lambda m: m.text == "🆕 Новый кальян")
async def new_hookah(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_last_choice.pop(user_id, None)

    await state.set_state(MixForm.choosing_base)
    await message.answer(
        "🆕 Делаем новый кальян!\nКакую основу выбираем?",
        reply_markup=base_keyboard()
    )

# ================== ЗАПУСК ==================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
