import asyncio
import logging
import sys
from os import getenv
from aiogram import F
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import sqlite3
from PIL import Image
import io

TOKEN = ''
dp = Dispatcher()
korzina = []


async def send_resized_image_to_telegram(chat_id, photo, bot):
    resized_image = resize_image(photo)
    with io.BytesIO(await resized_image) as file:
        await bot.send_photo(chat_id, file)


async def resize_image(image_data, size=(200, 200)):
    image = Image.open(io.BytesIO(image_data))  # Открываем изображение из бинарных данных
    image = image.resize(size)  # Изменяем размер изображения
    output = io.BytesIO()  # Создаем буфер для вывода
    image.save(output, format='PNG')  # Сохраняем изображение в формате PNG
    return output.getvalue()  # Возвращаем измененное изображение как бинарные данные


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    kb = [[types.KeyboardButton(text="Выбрать товар"), types.KeyboardButton(text="Служба поддержки")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Здравствуй, {hbold(message.from_user.full_name)}! Выберите действие", reply_markup=keyboard)


@dp.message(F.text.lower() == "выбрать товар")
async def with_puree(message: types.Message):
    kb = [
            [types.KeyboardButton(text="Вернутся на главную ⬅"), types.KeyboardButton(text="Корзина")],
            [types.KeyboardButton(text="🌿 Рапэ племенное 🧘🏼‍♂"), types.KeyboardButton(text="🍄 Мухоморы  шляпки 🍄")],
            [types.KeyboardButton(text="🦔 Цельный гриб 🦔"), types.KeyboardButton(text="💊 Микродозинг в капсулах 💊")],
            [types.KeyboardButton(text="⭐ Молотый ⭐"), types.KeyboardButton(text="🥤 Настойки 🥤")],
            [types.KeyboardButton(text="🍄 Мухоморные крема 🍄"), types.KeyboardButton(text="🌱 Чай 🌱")],
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите категорию", reply_markup=keyboard)


#Done
@dp.message(F.text.lower() == "🍄 мухоморы  шляпки 🍄")
async def with_puree_muhamor(message: types.Message):
    name_one_filter = []
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM list_gribs WHERE topic='Шляпки'")
    records = cursor.fetchall()

    record_photo = cursor.fetchone()
    if record_photo:
        image_data = record_photo[0]
        size = (200, 200)

        # Создаем изображение из данных BLOB и изменяем его размер
        image = Image.open(io.BytesIO(image_data))
        image = image.resize(size)

        # Создаем буфер для сохранения изображения в формате PNG
        output = io.BytesIO()
        image.save(output, format='PNG')

        # Получаем бинарные данные из буфера
        image_bytes = output.getvalue()

    kb = [
        [types.KeyboardButton(text="Назад ⬅")],
        [types.KeyboardButton(text="Корзина")],
    ]
    for i in range(0, len(records), 2):
        record_current = records[i][1]
        if i + 1 < len(records):  # Проверяем, что следующая запись существует
            record_next = records[i + 1][1]
            kb.append([types.KeyboardButton(text=f"Товар: {record_current}"),
                       types.KeyboardButton(text=f"Товар: {record_next}")])
        else:
            kb.append([types.KeyboardButton(text=f"Товар: {record_current}")])

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"🌿 Добро пожаловать в раздел: 🍄 Мухоморы  шляпки 🍄\n\n"
                         "Чтобы добавить товар в корзину, просто нажмите на него и проследуйте инструкции.\n\n"
                         "⚖️ Все товары имею разный вес. ⚖",
                         reply_markup=keyboard)

    @dp.message(lambda message: message.text.startswith("Товар:"))
    async def show_product_details_muhamor(message: types.Message):
        name = message.text.split(": ")[1]
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM list_gribs WHERE name=?", (name,))
        records = cursor.fetchall()
        if len(records) > 0:
            kb = [
                [types.KeyboardButton(text="Назад ⬅"), types.KeyboardButton(text="Добавить в корзину")],
                [types.KeyboardButton(text="Ввести количество товара")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

            name_one_filter.append(f"{name} {records[0][2]} {records[0][3]}")
            await message.answer(f"Вы выбрали товар: {name}\n\nДополнительная информация о товаре:\nВес: {records[0][2]}⚖\nЦена: {records[0][3]}💵", reply_markup=keyboard)

    @dp.message(lambda message: message.text == "Добавить в корзину")
    async def request_quantity_1(message: types.Message):
        kb = [[types.KeyboardButton(text="Меню 🍄 Мухоморы  шляпки 🍄⬅")], [types.KeyboardButton(text="Корзина")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f"Продукт {name_one_filter[0]} добавлен в корзину\nКоличество 1 шт", reply_markup=keyboard)
        korzina.append(f"{name_one_filter[0][0:]} 1 шт")
        name_one_filter.clear()

        @dp.message(lambda message: message.text == "Меню 🍄 Мухоморы  шляпки 🍄⬅")
        async def record_quantity_1(message: types.Message):
            await with_puree_muhamor(message)

    @dp.message(lambda message: message.text == "Ввести количество товара")
    async def request_quantity_2(message: types.Message):
        kb = [[types.KeyboardButton(text="Главное меню ⬅")], [types.KeyboardButton(text="1"), types.KeyboardButton(text="2"), types.KeyboardButton(text="3")],[types.KeyboardButton(text="4"), types.KeyboardButton(text="5"), types.KeyboardButton(text="6")],[types.KeyboardButton(text="7"), types.KeyboardButton(text="8"), types.KeyboardButton(text="9")], [types.KeyboardButton(text="10")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Введите количество товара:", reply_markup=keyboard)

        @dp.message(lambda message: message.text.isdigit())
        async def record_quantity_2(message: types.Message):
            quantity = int(message.text)
            kb = [[types.KeyboardButton(text="Главное меню ⬅"), types.KeyboardButton(text="Корзина")]]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            # quantity - переменная, которая содержит количество товаров, далее количество товаров мы добавляем в корзину
            # и далее пользователь может перейти в коризну
            await message.answer(f"Вы добавили в корзину: 🌿 {name_one_filter[0]}\n\nВ количестве: {quantity} штук", reply_markup=keyboard)
            korzina.append(f'{name_one_filter[0][0:]} {quantity} шт')
            name_one_filter.clear()


#Done
@dp.message(F.text.lower() == "🌿 рапэ племенное 🧘🏼‍♂")
async def with_puree_rape(message: types.Message):
    name_one_filter = []
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM list_gribs WHERE topic='Рапэ' ")
    records = cursor.fetchall()
    kb = [
        [types.KeyboardButton(text="Назад ⬅")],
        [types.KeyboardButton(text="Корзина")],
    ]
    for i in range(0, len(records), 2):
        record_current = records[i][1]
        if i + 1 < len(records):  # Проверяем, что следующая запись существует
            record_next = records[i + 1][1]
            kb.append([types.KeyboardButton(text=f"Товар: {record_current}"),
                       types.KeyboardButton(text=f"Товар: {record_next}")])
        else:
            kb.append([types.KeyboardButton(text=f"Товар: {record_current}")])

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("🌿 Добро пожаловать в раздел: Рапэ племенное! 🌿\n\n"
                         "Чтобы добавить товар в корзину, просто нажмите на него и проследуйте инструкции.\n\n"
                         "⚖️ Все товары из этого раздела имеют вес 5 грамм. ⚖️",
                         reply_markup=keyboard)

    @dp.message(lambda message: message.text.startswith("Товар:"))
    async def show_product_details_rape(message: types.Message):
        name = message.text.split(": ")[1]
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM list_gribs WHERE name=?", (name,))
        records = cursor.fetchall()
        if len(records) > 0:
            kb = [
                [types.KeyboardButton(text="Назад ⬅"), types.KeyboardButton(text="Добавить в корзину")],
                [types.KeyboardButton(text="Ввести количество товара")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

            name_one_filter.append(f"{name} {records[0][2]} {records[0][3]}")
            await message.answer(f"Вы выбрали товар: {name}\n\nДополнительная информация о товаре:\nВес: {records[0][2]}⚖\nЦена: {records[0][3]}💵", reply_markup=keyboard)
            print(f'{name_one_filter}')

    @dp.message(lambda message: message.text == "Добавить в корзину")
    async def request_quantity_1_rape(message: types.Message):
        kb = [[types.KeyboardButton(text="Меню 🌿 Рапэ племенное! 🌿⬅")], [types.KeyboardButton(text="Корзина")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f"Продукт {name_one_filter[0]} добавлен в корзину\nКоличество 1 шт", reply_markup=keyboard)
        korzina.append(f"{name_one_filter[0][0:]} 1 шт")
        name_one_filter.clear()

        @dp.message(lambda message: message.text == "Меню 🌿 Рапэ племенное! 🌿⬅")
        async def record_quantity_1_rape(message: types.Message):
            await with_puree_rape(message)

    @dp.message(lambda message: message.text == "Ввести количество товара")
    async def request_quantity_2_rape(message: types.Message):
        kb = [[types.KeyboardButton(text="Главное меню ⬅")], [types.KeyboardButton(text="1"), types.KeyboardButton(text="2"), types.KeyboardButton(text="3")],[types.KeyboardButton(text="4"), types.KeyboardButton(text="5"), types.KeyboardButton(text="6")],[types.KeyboardButton(text="7"), types.KeyboardButton(text="8"), types.KeyboardButton(text="9")], [types.KeyboardButton(text="10")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Введите количество товара:", reply_markup=keyboard)

        @dp.message(lambda message: message.text.isdigit())
        async def record_quantity_2_rape(message: types.Message):
            quantity = int(message.text)
            kb = [[types.KeyboardButton(text="Главное меню ⬅"), types.KeyboardButton(text="Корзина")]]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            # quantity - переменная, которая содержит количество товаров, далее количество товаров мы добавляем в корзину
            # и далее пользователь может перейти в коризну
            await message.answer(f"Вы добавили в корзину: 🌿 {name_one_filter[0]}\n\nВ количестве: {quantity} штук", reply_markup=keyboard)
            korzina.append(f'{name_one_filter[0][0:]} {quantity} шт')
            name_one_filter.clear()

    @dp.message(lambda message: message.text == "Назад ⬅")
    async def request_quantity_3_rape(message: types.Message):
        await with_puree_rape(message)

@dp.message(F.text.lower() == "служба поддержки")
async def without_puree(message: types.Message):
    await message.answer("Отличный выбор!")




@dp.message(F.text.lower() == "корзина")
async def korzina_main_list(message: types.Message):
    if len(korzina) != 0:
        print(korzina)
        kd = [
            [types.KeyboardButton(text=f"Отчистить"), types.KeyboardButton(text=f"Удалить определённые товары")]
        ]
        for product in korzina:
            kd.append([types.KeyboardButton(text=f"{product}")])

        keyboard = types.ReplyKeyboardMarkup(keyboard=kd, resize_keyboard=True)
        await message.answer(f"Вы перешли в меню корзины",
                             reply_markup=keyboard)
    else:
        kd = [
            [types.KeyboardButton(text=f"Приступить к покупкам 🛍")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kd, resize_keyboard=True)
        await message.answer(f"Вы перешли в меню корзины\n\nУ вас нет выбранных товаров 😔",
                             reply_markup=keyboard)

        @dp.message(F.text.lower() == "приступить к покупкам 🛍")
        async def start_shopping(message: types.Message):
            await with_puree(message)


@dp.message(F.text.lower() == "вернутся на главную ⬅")
async def without_puree(message: types.Message):
    kb = [[types.KeyboardButton(text="Выбрать товар"), types.KeyboardButton(text="Служба поддержки")], [types.KeyboardButton(text="Корзина")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Выберите действие", reply_markup=keyboard)


async def main() -> None:
    # Инициализируйте оба экземпляра с помощью defaultparsemode, который будет передаваться всем вызовам API
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # И диспетчеризация событий запуска
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


