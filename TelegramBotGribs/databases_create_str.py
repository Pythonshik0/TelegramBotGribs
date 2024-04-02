import sqlite3
import pandas as pd


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def bot_gribs(id, name, wt, cash, topic, photo):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        cursor.execute("""CREATE TABLE IF NOT EXISTS list_gribs 
            (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                wt TEXT NOT NULL,
                cash INT NOT NULL,
                topic TEXT NOT NULL,
                photo BLOB NULL
            )
        """)
        sqlite_connection.commit()

        sqlite_insert_blob_query = """INSERT INTO list_gribs
                                  (id, name, wt, cash, topic, photo) VALUES (?, ?, ?, ?, ?, ?)"""

        emp_photo = convert_to_binary_data(photo)
        # Преобразование данных в формат кортежа
        data_tuple = (id, name, wt, cash, topic, emp_photo)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()
        print("Данные успешно загружены в таблицу")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


#🌿 🇧🇷 Рапэ племенное🇧🇷 🐲🏹💘🌿 🧘🏼‍♂
bot_gribs(1, "Рапэ Нукини ягуар", "5 грамм", "1800₽", "Рапэ", "images/test_image.png")

#🍄 Мухоморы  шляпки🍄
bot_gribs(28, "Шляпки красного 🍄", "50 грамм", "1500₽", "Шляпки", "images/test_image.png")

#🍄 Шляпки пантерного 🍄
bot_gribs(30, "Шляпки пантерного 🍄", "50 грамм", "3000₽", "Шляпки", "images/test_image.png")

#🦔Цельный гриб
bot_gribs(32, "Ежовик", "100 грамм", "850₽", "Целый гриб", "images/test_image.png")

#💊 Микродозинг в капсулах 💊
bot_gribs(39, "Пантерный мухомор(капсулы)", "60 капсул по 0.4 грамм", "3000₽", "Капуслы", "images/test_image.png")

#⭐МОЛОТЫЙ
bot_gribs(53, "Ежовик гребенчатый молотый", "100 грамм", "990₽", "Молотые", "images/test_image.png")

#🥤НАСТОЙКА КРАСНОГО МУХОМОРА 50 мл 600₽
bot_gribs(59, "🥤НАСТОЙКА КРАСНОГО МУХОМОРА", "50 мл", "600₽", "Настойки", "images/test_image.png")

#🍄МУХОМОРНЫЕ КРЕМА
bot_gribs(60, "Дневной", "50 мл", "350₽", "Крема", "images/test_image.png")

#🍄МАЗЬ МУХОМОР
bot_gribs(68, "От псориаза", "40 мл", "370₽", "Мази", "images/test_image.png")

#Загрузка в таблицу exel
# sqlite_connection = sqlite3.connect('sqlite_python.db')
# df = pd.read_sql('select * from list_gribs', sqlite_connection)
# df.to_excel(r'C:\Users\User\Desktop/result.xlsx', index=False)