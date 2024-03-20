import datetime
import time

from APP.GS.test import GoogleSheetsManager
from APP.UTILS.db_commands import UserDatabase
gsm = GoogleSheetsManager('credentials.json', '1JED99HzVcXP6HtQJ-vFHibCl1HB8TuESITHG_mL6J98')
database = UserDatabase("users.db")

Time_list = [
    "0:00",
    "1:00",
    "2:00",
    "3:00",
    "4:00",
    "5:00",
    "6:00",
    "7:00",
    "8:00",
    "9:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00",
    "22:00",
    "23:00",
]

import sqlite3

def fetch_columns_from_database(db_name, table_name, column1, column2):
    # Подключение к базе данных
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Выполнение запроса и извлечение данных
    cur.execute(f"SELECT {column1}, {column2} FROM {table_name}")
    rows = cur.fetchall()
    users_list = [f'{row[0]} {row[1]}' for row in rows]
    # Закрытие соединения с базой данных
    cur.close()
    conn.close()

    # Возвращение результатов
    return users_list




while True:
    if gsm.exist_sheet(f'{datetime.datetime.now().strftime("%d.%m.%Y %H Plan")}') == False:
        list = fetch_columns_from_database('users.db','users', 'surname', 'name')
        print(list)
        gsm.create_sheet(f'{datetime.datetime.now().strftime("%d.%m.%Y %H Plan")}', 30, 25)
        gsm.add_employees(list)
        gsm.add_dates(Time_list)
    else:
        print('GG')
        pass
    time.sleep(10)