import datetime
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
from APP.UTILS.states_admin import get_user_plan_today
from APP.settings import Plan_sheet_key, Time_list, credentials_file
async def check_plan(message: Message, state: FSMContext):
    database = UserDatabase("users.db")
    GS_plan = GoogleSheetsManager(credentials_file, Plan_sheet_key)
    # ПОХУЙ
    if await database.search_user_by_id(message.from_user.id) == 0:
        await message.answer(
            f"<b>Привет, пользователь</b>\n Вы не зарегистрированны. Прошу обратитесь к менеджеру"
        )
    elif await database.search_user_by_id(message.from_user.id) == 1:
        id = message.from_user.id
        full_name = await database.search_user_by_id_plan_list(id)
        GS_plan.create_sheet(f'{datetime.datetime.now().strftime("%d.%m.%Y Plan")}', 30, 25)
        list =  GS_plan.get_values(full_name)
        print(full_name)
        await message.answer(f" {full_name} Лови \n {list}",reply_markup=user_reply_start)
    # Если админ
    elif await database.search_user_by_id(message.from_user.id) >= 2:
        await message.answer(
            f"Введите id телеграма пользователя.\n Просмотреть список пользователей можно с помощь команды.",
            reply_markup=cancel_button,
        )
        # Написать стейт для выбора пользователя
        # СТЕЙТ СОСТОИТ ИЗ ОДНОГО ПАРАМЕТРА. id Пользователя
        await state.set_state(get_user_plan_today.GET_ID)

async def check_plan_id(message: Message, state: FSMContext):
        # Проверка команды отмены
    database = UserDatabase("users.db")
    GS_plan = GoogleSheetsManager(credentials_file, Plan_sheet_key)
    id = await database.search_user_by_id_admin(message.text)
    if str(message.text) == "Стоп":
        await message.answer("Вы отменили заполнение", reply_markup=admin_reply_start)
        await state.clear()
        return
    # Проверка правильности id
    # ТУТ КОСЯК С ПОИСКОМ ПОЛЬЩОВАТЕЛЯ!!! ПРОВЕРИТЬ ВЕЗДЕ, КОГДА ПОДТЯНУ ПОЛЬЗОВАТЕЛЕЙ И БД
    elif str(id) == "0":
        await message.answer(f" Пользователь с id {message.text} не был найден. Проверьте правильность и запишите еще раз",reply_markup=cancel_button)
        await state.set_state(get_user_plan_today.GET_ID)
        return
        # Если все ок
    else:
        await state.update_data(id=message.text)
        context_data = await state.get_data()
        full_name = await database.search_user_by_id_plan_list(context_data['id'])
        print(full_name)
        GS_plan.create_sheet(f'{datetime.datetime.now().strftime("%d.%m.%Y Plan")}', 30, 25)
        list =  GS_plan.get_values(full_name)
        await message.answer(f" {full_name} \n {list}",reply_markup=admin_reply_start)
    
        
        
        await state.clear()