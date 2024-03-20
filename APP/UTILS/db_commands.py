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
            await cursor.execute("SELECT * FROM users WHERE id_tg=?", (id_tg,))
            user = await cursor.fetchone()
            if user is not None:
                await cursor.execute(f"DELETE FROM users WHERE id_tg = {str(id_tg)}")
                await db.commit()
                print(id_tg, 'УДФЛЕН')
            else:
                print("User delited earler.")

    # Поиск пользователя
    async def search_user_by_id(self, id_tg):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()
            await cursor.execute(f"SELECT * FROM users WHERE id_tg=?", (id_tg,))
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
    
    async def search_user_by_id_plan_list(self, id_tg):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users WHERE id_tg=?", (id_tg,))
            user = await cursor.fetchone()

            if user is not None:
                return f'{user[2]} {user[1]}'
            else:
                print("User not found.")
                return 0


    
    async def users_list(self):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users")
            rows = await cursor.fetchall()
            users_list = "\n".join([f"{row[2]} - {row[1]}. ID = {row[0]}. Доступ {row[3]}" for row in rows])
            return users_list
    # Написать функцию для чек план. На вход id, на выход имя и фамилия
    # Просмотр пользователей
        
    async def users_list_sheet(self):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT surname, name FROM users")
            rows = await cursor.fetchall()
            users_list = [f'{row[0]} {row[1]}' for row in rows]
            return users_list



    # Смена прав
    async def change_permission(self, id_tg, permission):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users WHERE id_tg=?", (id_tg,))
            user = await cursor.fetchone()
            if user is not None:
                await cursor.execute(f"UPDATE users SET permission = '{permission}' WHERE id_tg = {id_tg}")
                await db.commit()
                print(id_tg, 'Изменены права')
            else:
                print("User delited earler.")
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
