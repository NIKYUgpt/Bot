import datetime
from aiogram import Bot # type: ignore
from aiogram.types import Message # type: ignore
from aiogram.fsm.context import FSMContext # type: ignore


from APP.GS.test import GoogleSheetsManager
from APP.UTILS.db_commands import UserDatabase

from APP.KEYBOARDS.admin_reply import admin_reply_start
from APP.KEYBOARDS.user_reply import user_reply_start
from APP.KEYBOARDS.reply import (
    time_selector,
    cancel_button,
    date_selector,
    start_button,
)

from APP.UTILS.states_admin import add_employer, delete_employeer, change_permissions
from APP.settings import Plan_sheet_key, Time_list, credentials_file


# =======================================================================================================================
# Функция добавления сотрудника
async def add_new_employer(message: Message, state: FSMContext):
    database = UserDatabase("users.db")
    # ПОХУЙ
    if await database.search_user_by_id(message.from_user.id) == 0:
        await message.answer(
            f"<b>Привет, пользователь</b>\n Вы не зарегистрированны. Прошу обратитесь к менеджеру"
        )
    # Если зарегистрирован
    elif await database.search_user_by_id(message.from_user.id) == 1:
        await message.answer(f"<b>недостаточно прав</b>", reply_markup=user_reply_start)
    # Если админ
    elif await database.search_user_by_id(message.from_user.id) >= 2:
        await message.answer(
            f"Создание пользователя.\nВведите id телеграма пользователя.",
            reply_markup=cancel_button,
        )
        await state.set_state(add_employer.GET_ID)

async def add_new_employer_id(message: Message, state: FSMContext):
    database = UserDatabase("users.db")
    id = await database.search_user_by_id_admin(message.text)
    #print(message.text.isdigit())
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Проверка правильности id
    elif str(id) != "0":
        await message.answer(
            f" Пользователь с id {message.text} уже есть. Проверьте правильность и запишите еще раз",
            reply_markup=cancel_button,
        )
        await state.set_state(add_employer.GET_ID)
    # Проверка цифрового значения
    elif message.text.isdigit() == False:
        await message.answer(
            f"Некоректное значение {message.text}. Проверьте правильность и запишите еще раз",
            reply_markup=cancel_button,
        )
        await state.set_state(add_employer.GET_ID)
        return
    # Если все ок
    else:
        await message.answer(
            f"Если {message.text} - неверно,\n то нажмите стоп и запустите еще раз.\n Если все верно, напишите имя сотрудника.",
            reply_markup=cancel_button,
        )
        await state.update_data(id=message.text)
        await state.set_state(add_employer.GET_NAME)

async def add_employer_name(message: Message, state: FSMContext):
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Если все ок
    else:
        await message.answer(
            f"Имя - {str(message.text)},\nЕсли неверно, то нажмите стоп и запустите еще раз.\n Если все верно, напишите фамилию сотрудника",
            reply_markup=cancel_button,
        )
        await state.update_data(name=message.text)
        await state.set_state(add_employer.GET_SURNAME)

async def add_employer_surname(message: Message, state: FSMContext):
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Если все ок
    else:
        await message.answer(
            f"Фамилия - {str(message.text)},\nЕсли неверно, то нажмите стоп и запустите еще раз.\n Если все верно, напишите права доступа к боту.\nЕсли Просто сотрудник, то 1, если менеджер, то 2 и более",
            reply_markup=cancel_button,
        )
        await state.update_data(surname=message.text)
        await state.set_state(add_employer.GET_PERMISSION)

async def add_employer_permission(message: Message, state: FSMContext):
    # Проверка команды отмены
    GS_plan = GoogleSheetsManager(credentials_file, Plan_sheet_key)
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Проверка Времени
    elif message.text.isdigit() == False or int(message.text) <= 0:
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=cancel_button,
        )
        await state.set_state(add_employer.GET_PERMISSION)
        return
    # Если все ок
    else:
        await message.answer(f"{message.text} - права. готово")
        await state.update_data(permission=message.text)
        context_data = await state.get_data()
        database = UserDatabase("users.db")
        #print(context_data)
        await database.add_user(context_data['id'], context_data['name'], context_data['surname'], context_data["permission"])
        # =======================================================================================
        GS_plan.create_sheet(f'{datetime.datetime.now().strftime("%d.%m.%Y Plan")}', 30, 25)
        surname = context_data['surname']
        name = context_data['name']
        GS_plan.add_employee(f'{surname} {name}')
        # =======================================================================================
        await message.answer(f"{str(context_data)}", reply_markup=admin_reply_start)
        await state.clear()

# =======================================================================================================================
# Функция Удаления сотрудника
async def delete_employer(message: Message, state: FSMContext):
    database = UserDatabase("users.db")
    # ПО��У��
    if await database.search_user_by_id(message.from_user.id) == 0:
        await message.answer(
            f"<b>Привет, пользователь</b>\n Вы не зарегистрированны. Прошу обратитесь к менеджеру"
        )
    # Если зарегистрирован
    elif await database.search_user_by_id(message.from_user.id) == 1:
        await message.answer(f"<b>недостаточно прав</b>", reply_markup=user_reply_start)
    # Если админ
    elif await database.search_user_by_id(message.from_user.id) >= 2:
        await message.answer(f"<b>Введите id пользователя</b>", reply_markup=cancel_button)
        await state.set_state(delete_employeer.GET_ID)
        
async def delete_employer_id(message: Message, state: FSMContext):
        # Проверка команды отмены
    database = UserDatabase("users.db")
    # Тестовый
    id = await database.search_user_by_id_admin(message.text)
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Проверка правильности id
    # ТУТ КОСЯК С ПОИСКОМ ПОЛЬЩОВАТЕЛЯ!!! ПРОВЕРИТЬ ВЕЗДЕ, КОГДА ПОДТЯНУ ПОЛЬЗОВАТЕЛЕЙ И БД
    elif str(id) == "0":
        await message.answer(f" Пользователь с id {message.text} не был найден. Проверьте правильность и запишите еще раз",reply_markup=cancel_button)
        await state.set_state(delete_employeer.GET_ID)
        return
        # Если все ок
    else:
        await message.answer(f"Пользователь с id {message.text} удален", reply_markup=admin_reply_start)
        await state.update_data(id=message.text)
        # Тестовый
        context_data = await state.get_data()
        await message.answer(f"{str(context_data)}", reply_markup=admin_reply_start)
        await database.delete_user(context_data['id'])

        await state.clear()
        
# =======================================================================================================================
# Функция изменения прав сотрудника
async def edit_employer_permisson(message: Message, state: FSMContext):
    database = UserDatabase("users.db")
    # ПО��У��
    if await database.search_user_by_id(message.from_user.id) == 0:
        await message.answer(
            f"<b>Привет, пользователь</b>\n Вы не зарегистрированны. Прошу обратитесь к менеджеру"
        )
    # Если зарегистрирован
    elif await database.search_user_by_id(message.from_user.id) == 1:
        await message.answer(f"<b>недостаточно прав</b>", reply_markup=user_reply_start)
    # Если админ
    elif await database.search_user_by_id(message.from_user.id) >= 2:
        await message.answer(f"<b>Введите id пользователя</b>", reply_markup=cancel_button)
        await state.set_state(change_permissions.GET_ID)
        
async def edit_employer_permisson_id(message: Message, state: FSMContext):
        # Проверка команды отмены
    database = UserDatabase("users.db")
    id = await database.search_user_by_id_admin(message.text)
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Проверка правильности id
    elif str(id) == "0":
        await message.answer(f" Пользователь с id {message.text} не был найден. Проверьте правильность и запишите еще раз",reply_markup=cancel_button)
        await state.set_state(change_permissions.GET_ID)
        return
        # Если все ок
    else:
        await message.answer(f"Пользователь с id {message.text} Найден.\n Введите право доступа", reply_markup=cancel_button)
        await state.update_data(id=message.text)
        await state.set_state(change_permissions.GET_PERMISSION)
        
async def edit_employer_permisson_permission(message: Message, state: FSMContext):
        # Проверка команды отмены
    database = UserDatabase("users.db")
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Проверка правильности id
    elif int(message.text) <= 0:
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=cancel_button,
        )
        await state.set_state(change_permissions.GET_PERMISSION)
    else:
        await message.answer(f"Права уровня {message.text} выданы", reply_markup=admin_reply_start)
        await state.update_data(permissions=message.text)
        context_data = await state.get_data()
        await message.answer(f"{str(context_data)}", reply_markup=admin_reply_start)
        await database.change_permission(context_data['id'], context_data['permissions'])
        await state.clear()

# =======================================================================================================================
# Функция просмотра списка сотрудников
async def employers_list(message: Message, bot: Bot):
    database = UserDatabase("users.db")
    await database.create_table()
    # Если права => 1, то админ, если 0, то пользователь, если none, то не пускать
    # Если не зарегистрирован
    if await database.search_user_by_id(message.from_user.id) == 0:
        await message.answer(
            f"<b>Привет, пользователь</b>\n Вы не зарегистрированны. Прошу обратитесь к менеджеру"
        )
    # Если зарегистрирован
    elif await database.search_user_by_id(message.from_user.id) == 1:
        await message.answer(f"Нет доступа", reply_markup=user_reply_start)
    # Если админ
    elif await database.search_user_by_id(message.from_user.id) >= 2:
        #Тут команда выдачи списка
        list = await database.users_list()
        await message.answer(f"<b>Лови</b>\n\n{list}", reply_markup=admin_reply_start)
        #print('=============================================================\n\n\n\n\n')
        

# =======================================================================================================================
# 
