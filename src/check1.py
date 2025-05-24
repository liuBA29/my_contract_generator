import sqlite3
from config import *

# Подключение к базе данных


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# # Запрос на выборку всех данных из таблицы
# cursor.execute("SELECT * FROM completion_of_work")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)


cursor.execute("SELECT * FROM customers")
# Получение всех строк из результата запроса
rows = cursor.fetchall()
# Вывод данных
for row in rows:
    print(row)





#
# cursor.execute("SELECT * FROM payment_terms")
# rows = cursor.fetchall()
#
# for row in rows:
#     print(row)



# # Запрос структуры таблицы completion_of_work
# cursor.execute("")
# columns = cursor.fetchall()
#
# # Вывод имен колонок
# print("Колонки в таблице completion_of_work:")
# for column in columns:
#     print(column[1])  # Имя колонки находится во втором элементе кортежа

# Закрытие подключения
conn.close()


# Закрытие подключения

