from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


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

from APP.UTILS.states_admin import add_plan_admin
from APP.UTILS.states_user import add_plan_user, add_fact_user
from APP.settings import Plan_sheet_key, Time_list, credentials_file

from APP.settings import Date_list, Time_list


# ========================================================================
# Команда /Start и проверка прав
async def get_start(message: Message, bot: Bot):
    #
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
        await message.answer(f"<b>Привет</b>", reply_markup=user_reply_start)
    # Если админ
    elif await database.search_user_by_id(message.from_user.id) >= 2:
        await message.answer(f"<b>Привет Админ!</b>", reply_markup=admin_reply_start)


# ========================================================================
# Команда Добавить План
# Тут есть разделение на админа и пользователя


async def add_plan(message: Message, state: FSMContext):
    database = UserDatabase("users.db")
    # ПОХУЙ
    if await database.search_user_by_id(message.from_user.id) == 0:
        await message.answer(
            f"<b>Привет, пользователь</b>\n Вы не зарегистрированны. Прошу обратитесь к менеджеру"
        )
    # Если зарегистрирован
    # GET_PROJECT_NAME = State()
    # GET_START_TIME = State()
    # GET_END_TIME = State()
    # GET_DATE = State()
    elif await database.search_user_by_id(message.from_user.id) == 1:
        await message.answer(f"Введите название проекта", reply_markup=cancel_button)
        await state.set_state(add_plan_user.GET_PROJECT_NAME)
        await state.update_data(id=message.from_user.id)

    # Если админ
    # ID = State ()
    # GET_PROJECT_NAME = State()
    # GET_START_TIME = State()
    # GET_END_TIME = State()
    # GET_DATE = State()
    elif await database.search_user_by_id(message.from_user.id) >= 2:
        await message.answer(
            f"Заполнение плана пользователю. \n Введите id телеграма пользователя.\n Просмотреть список пользователей можно с помощь команды.",
            reply_markup=cancel_button,
        )
        await state.set_state(add_plan_admin.GET_ID)


# План Админ
async def get_id_admin(message: Message, state: FSMContext):
    database = UserDatabase("users.db")
    id = await database.search_user_by_id_admin(message.text)
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Проверка правильности id
    # ТУТ КОСЯК С ПОИСКОМ ПОЛЬЩОВАТЕЛЯ!!! ПРОВЕРИТЬ ВЕЗДЕ, КОГДА ПОДТЯНУ ПОЛЬЗОВАТЕЛЕЙ И БД
    elif str(id) == "0":
        await message.answer(
            f" Пользователь с id {message.text} не был найден. Проверьте правильность и запишите еще раз",
            reply_markup=cancel_button,
        )
        await state.set_state(add_plan_admin.GET_ID)
        return
    # Если все ок
    else:
        await message.answer(
            f"Если это не тот сотрудник ({str(message.text)}) - {str(id)},\n то нажмите стоп и запустите еще раз.\n Если все верно, напишите название проекта.",
            reply_markup=cancel_button,
        )
        await state.update_data(id=message.text)
        await state.set_state(add_plan_admin.GET_PROJECT_NAME)


# ==================================================================================


async def get_project_name_admin(message: Message, state: FSMContext):
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Если все ок
    else:
        await message.answer(
            f"{message.text} - Название проекта. Если это не то название, то нажмите стоп и запустите еще раз.\nЕсли все верно, напишите время начала проекта.\n Выберите время из списка снизу.",
            reply_markup=time_selector,
        )
    await state.update_data(project_name=message.text)
    await state.set_state(add_plan_admin.GET_START_TIME)


# ==================================================================================


async def get_start_time_admin(message: Message, state: FSMContext):
    database = UserDatabase("users.db")
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Проверка Времени
    elif message.text not in Time_list:
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=time_selector,
        )
        await state.set_state(add_plan_admin.GET_START_TIME)
    # Если все ок
    else:
        await message.answer(
            f"{message.text} - Время начала. Если это не то время, то нажмите стоп и запустите еще раз.\nЕсли все верно, напишите время конца проекта.\n Выберите время из списка снизу.",
            reply_markup=time_selector,
        )
        await state.update_data(start_time=message.text)
        await state.set_state(add_plan_admin.GET_END_TIME)


# ==================================================================================


async def get_end_time_admin(message: Message, state: FSMContext):
    context_data = await state.get_data()
    end_time = message.text
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Проверка Времени
    elif message.text not in Time_list:
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=time_selector,
        )
        await state.set_state(add_plan_admin.GET_END_TIME)
    # Проверка указания времени
    elif int(context_data["start_time"].split(":")[0]) > int(end_time.split(":")[0]):
        await message.answer(
            f" Некорректное заполнение - {message.text} не может быть меньше времени начала. Проверьте правильность и запишите еще раз",
            reply_markup=time_selector,
        )
        await state.set_state(add_plan_admin.GET_END_TIME)
    # Если все ок
    else:
        await message.answer(
            f"{message.text} - Время конца. Если это не то время, то нажмите стоп и запустите еще раз.\nЕсли все верно, напишите время конца проекта.\n Выберите дату из списка снизу.",
            reply_markup=date_selector,
        )
        await state.update_data(end_time=message.text)
        await state.set_state(add_plan_admin.GET_DATE)


# ==================================================================================


async def get_date_admin(message: Message, state: FSMContext):
    # Проверка команды отмены
    database = UserDatabase("users.db")
    GS_plan = GoogleSheetsManager(credentials_file, Plan_sheet_key)
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Проверка Времени
    elif message.text not in Date_list:
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=date_selector,
        )
        await state.set_state(add_plan_admin.GET_DATE)
    # Если все ок
    else:
        await message.answer(f"{message.text} - дата. готово")
        await state.update_data(date=message.text)
        context_data = await state.get_data()
        name = await database.search_user_by_id_plan_list(context_data['id'])
        print(name)
        st = context_data['start_time']
        et = context_data['end_time']
        date = context_data['date']
        project_name = context_data['project_name']
        users_list = await database.users_list_sheet()
        print(f"\n\n\n\n\n\n\n")
        print(name)
        print(st)
        print(et)
        print(date)
        print(project_name)
        print(f"\n\n\n\n\n\n\n")

        if GS_plan.exist_sheet(f'{date} Plan') == False:
            GS_plan.create_sheet(f'{date} Plan', 30, 25)
            GS_plan.add_dates(Time_list)
            GS_plan.add_employees(users_list)
        else:
            GS_plan.create_sheet(f'{date} Plan', 30, 25)
        GS_plan.add_info(project_name, name, st, et)
        await message.answer(f"{str(context_data)}", reply_markup=admin_reply_start)
        await state.clear()


# Пользователь план


async def get_project_name_user(message: Message, state: FSMContext):
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=user_reply_start)
        await state.clear()
        return
    # Если все ок
    else:
        await message.answer(
            f"{message.text} - Название проекта. Если это не то название, то нажмите стоп и запустите еще раз.\nЕсли все верно, напишите время начала проекта.\n Выберите время из списка снизу.",
            reply_markup=time_selector,
        )
    await state.update_data(project_name=message.text)
    await state.set_state(add_plan_user.GET_START_TIME)


async def get_start_time_user(message: Message, state: FSMContext):
    
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=user_reply_start)
        await state.clear()
        return
    # Проверка Времени
    elif message.text not in Time_list:
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=time_selector,
        )
        await state.set_state(add_plan_user.GET_START_TIME)
    # Если все ок
    else:
        await message.answer(
            f"{message.text} - Время начала. Если это не то время, то нажмите стоп и запустите еще раз.\nЕсли все верно, напишите время конца проекта.\n Выберите время из списка снизу.",
            reply_markup=time_selector,
        )
        await state.update_data(start_time=message.text)
        await state.set_state(add_plan_user.GET_END_TIME)


# ==================================================================================


async def get_end_time_user(message: Message, state: FSMContext):
    context_data = await state.get_data()
    end_time = message.text
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=user_reply_start)
        await state.clear()
        return
    # Проверка Времени
    elif message.text not in Time_list:
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=time_selector,
        )
        await state.set_state(add_plan_user.GET_END_TIME)
    # Проверка указания времени
    elif int(context_data["start_time"].split(":")[0]) > int(end_time.split(":")[0]):
        await message.answer(
            f" Некорректное заполнение - {message.text} не может быть меньше времени начала. Проверьте правильность и запишите еще раз",
            reply_markup=time_selector,
        )
        await state.set_state(add_plan_user.GET_END_TIME)
    # Если все ок
    else:
        await message.answer(
            f"{message.text} - Время конца. Если это не то время, то нажмите стоп и запустите еще раз.\nЕсли все верно, напишите время конца проекта.\n Выберите дату из списка снизу.",
            reply_markup=date_selector,
        )
        await state.update_data(end_time=message.text)
        await state.set_state(add_plan_user.GET_DATE)


# ==================================================================================


async def get_date_user(message: Message, state: FSMContext):
    # Проверка команды отмены
    database = UserDatabase("users.db")
    GS_plan = GoogleSheetsManager(credentials_file, Plan_sheet_key)
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=user_reply_start)
        await state.clear()
        return
    # Проверка Времени
    elif message.text not in Date_list:
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=date_selector,
        )
        await state.set_state(add_plan_user.GET_DATE)
    # Если все ок
    else:
        await message.answer(f"{message.text} - дата. готово")
        await state.update_data(date=message.text)
        context_data = await state.get_data()
        # Часто надо
        name = await database.search_user_by_id_plan_list(context_data['id'])
        # ===============================================================
        print(name)
        st = context_data['start_time']
        et = context_data['end_time']
        date = context_data['date']
        project_name = context_data['project_name']
        users_list = await database.users_list_sheet()
        print(f"\n\n\n\n\n\n\n")
        print(name)
        print(st)
        print(et)
        print(date)
        print(project_name)
        print(f"\n\n\n\n\n\n\n")

        if GS_plan.exist_sheet(f'{date} Plan') == False:
            GS_plan.create_sheet(f'{date} Plan', 30, 25)
            GS_plan.add_dates(Time_list)
            GS_plan.add_employees(users_list)
        else:
            GS_plan.create_sheet(f'{date} Plan', 30, 25)
        GS_plan.add_info(project_name, name, st, et)
        await message.answer(f"{str(context_data)}", reply_markup=user_reply_start)
        await state.clear()


# ==================================================================================
# Добавить факт


async def add_fact(message: Message, state: FSMContext):
    database = UserDatabase("users.db")
    # ПОХУЙ
    if await database.search_user_by_id(message.from_user.id) == 0:
        await message.answer(
            f"<b>Привет, пользователь</b>\n Вы не зарегистрированны. Прошу обратитесь к менеджеру"
        )
    # Если зарегистрирован
    # GET_PROJECT_NAME = State()
    # GET_COMMENT = State()
    # GET_START_TIME = State()
    # GET_END_TIME = State()
    # GET_DATE = State()
    elif await database.search_user_by_id(message.from_user.id) >= 1:
        await message.answer(f"Введите название проекта", reply_markup=cancel_button)
        await state.set_state(add_fact_user.GET_PROJECT_NAME)
        await state.update_data(id=message.from_user.id)


# ==================================================================================


async def get_project_name_fact(message: Message, state: FSMContext):
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=start_button)
        await state.clear()
        return
    # Если все ок
    else:
        await message.answer(
            f"{message.text} - Название проекта. Если это не то название, то нажмите стоп и запустите еще раз.\nЕсли все верно, напишите Комментарий к проделанной работе проекта.",
            reply_markup=cancel_button,
        )
    await state.update_data(project_name=message.text)
    await state.set_state(add_fact_user.GET_COMMENT)


# ==================================================================================


async def get_comment_fact(message: Message, state: FSMContext):
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=start_button)
        await state.clear()
        return
    # Если все ок
    else:
        await message.answer(
            f"{message.text} - Комментарий. Если вы ошиблись в коментарии, то нажмите стоп и запустите еще раз.\nЕсли все верно, напишите время, во сколько начали выполнять проект.\nМожно указать свое время.",
            reply_markup=time_selector,
        )
    await state.update_data(project_comment=message.text)
    await state.set_state(add_fact_user.GET_START_TIME)


# ==================================================================================


async def get_start_time_fact(message: Message, state: FSMContext):
    time = message.text

    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=start_button)
        await state.clear()
        return
    # Проверка Времени
    elif (
        int(time.split(":")[0]) <= 0
        and int(time.split(":")[0]) >= 23
        and int(time.split(":")[1]) <= 0
        and int(time.split(":")[1]) >= 59
    ):
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=time_selector,
        )
        await state.set_state(add_fact_user.GET_START_TIME)
    # Если все ок
    else:
        await message.answer(
            f"{message.text} - Время начала. Если это не то время, то нажмите стоп и запустите еще раз.\nЕсли все верно, напишите время, во сколько закончили выполнять проект.\n Если время заходит на другой день, то напишите, что закончили в 23:59 текущего дня, и начали в 00:00 следующего дня. \nМожно указать свое время.",
            reply_markup=time_selector,
        )
        await state.update_data(start_time=message.text)
        await state.set_state(add_fact_user.GET_END_TIME)


# ==================================================================================


async def get_end_time_fact(message: Message, state: FSMContext):
    # Проверка команды отмены
    time = message.text
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=start_button)
        await state.clear()
        return
    # Проверка Времени
    elif (
        int(time.split(":")[0]) <= 0
        and int(time.split(":")[0]) >= 23
        and int(time.split(":")[1]) <= 0
        and int(time.split(":")[1]) >= 59
    ):
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=time_selector,
        )
        await state.set_state(add_fact_user.GET_END_TIME)
    # Если все ок
    else:
        await message.answer(
            f"{message.text} - Время конца. Если это не то время, то нажмите стоп и запустите еще раз.\nЕсли все верно, напишите время конца проекта.\n Выберите дату из списка снизу.",
            reply_markup=date_selector,
        )
        await state.update_data(end_time=message.text)
        await state.set_state(add_fact_user.GET_DATE)


async def get_date_fact(message: Message, state: FSMContext):
    # Проверка команды отмены
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=start_button)
        await state.clear()
        return
    # Проверка Времени
    elif message.text not in Date_list:
        await message.answer(
            f" Некорректное заполнение - {message.text}.Проверьте правильность и запишите еще раз",
            reply_markup=date_selector,
        )
        await state.set_state(add_fact_user.GET_DATE)
    # Если все ок
    else:
        await message.answer(f"{message.text} - дата. готово")
        await state.update_data(date=message.text)
        context_data = await state.get_data()
        database = UserDatabase("users.db")
        await database.create_table()

        # Если зарегистрирован
        if await database.search_user_by_id(message.from_user.id) == 1:
            await message.answer(f"{str(context_data)}", reply_markup=user_reply_start)
        # Если админ
        elif await database.search_user_by_id(message.from_user.id) >= 2:
            await message.answer(f"{str(context_data)}", reply_markup=admin_reply_start)
        await state.clear()
