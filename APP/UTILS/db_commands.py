import aiosqlite
import asyncio

# ========================================================================
# Класс датабазы
# Переменные: id_tg, name, surname, permission


class UserDatabase:
    def __init__(self, db_name):
        self.db_name = db_name

    # Создание таблицы
    async def create_table(self):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()
            await cursor.execute(
                "CREATE TABLE IF NOT EXISTS users (id_tg INTEGER PRIMARY KEY, name TEXT, surname TEXT, permission INTEGER)"
            )

    # Добавление пользователя
    async def add_user(self, id_tg, name, surname, permission):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users WHERE id_tg=?", (id_tg,))
            user = await cursor.fetchone()
            if user is not None:
                print("User exected.")
            else:
                await cursor.execute(
                    "INSERT INTO users (id_tg, name, surname, permission) VALUES (?, ?, ?, ?)",
                    (id_tg, name, surname, permission),
                )
                await db.commit()
                print("User added successfully.")

    # Удаление пользователя
    async def delete_user(self, id_tg):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()
            await cursor.execute("DELETE FROM users WHERE id_tg == ?", (id_tg,))

    # Поиск пользователя
    async def search_user_by_id(self, id_tg):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users WHERE id_tg=?", (id_tg,))
            user = await cursor.fetchone()

            if user is not None:

                return user[3]
            else:
                print("User not found.")
                return 0

    # Поиск пользователя для заполнения
    async def search_user_by_id_admin(self, id_tg):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users WHERE id_tg=?", (id_tg,))
            user = await cursor.fetchone()

            if user is not None:

                return user[2]
            else:
                print("User not found.")
                return 0


# Пример использования класса
"""
async def main():
    database = UserDatabase("users.db")
    
    await database.create_table()

    await database.add_user(1, "John", 25)
    await database.add_user(2, "Alice", 30)
    await database.add_user(3, "Bob", 27)

    await database.search_user_by_id(2)
    await database.search_user_by_id(4)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
"""

# ========================================================================
