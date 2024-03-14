from aiogram import F, Bot, Dispatcher
from aiogram.types import Message, ContentType
from aiogram.filters import Command

import asyncio
import logging

from APP.HANDLERS.basic import get_start
from APP.HANDLERS import admin_handlers, basic
from APP.UTILS.commands import set_commands
from APP.UTILS.states_user import add_fact_user, add_plan_user
from APP.settings import settings
from APP.UTILS.states_admin import add_plan_admin, add_employer, delete_employeer, change_permissions


# ========================================================================
# Функции уведомления
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text="bot start")


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="bot stop")


# ========================================================================
# Запуск бота
async def Start():
    bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")
    dp = Dispatcher()
    # ========================================================================
    # Отправление сообщение при старте и остановке
    # logging.basicConfig(level=logging.INFO,
    #                    format="%(asctime)s - [%(levelname)s] - %(name)s - "
    #                    "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # =======================================================================
    # Регистрация функций

    dp.message.register(get_start, Command(commands=["start", "run"]))

    # Регистрация добавить план
    dp.message.register(basic.add_plan, F.text == "Добавить План")
    # Регистрация админ добавить план
    dp.message.register(basic.get_id_admin, add_plan_admin.GET_ID)
    dp.message.register(basic.get_project_name_admin, add_plan_admin.GET_PROJECT_NAME)
    dp.message.register(basic.get_start_time_admin, add_plan_admin.GET_START_TIME)
    dp.message.register(basic.get_end_time_admin, add_plan_admin.GET_END_TIME)
    dp.message.register(basic.get_date_admin, add_plan_admin.GET_DATE)
    # Регистрация пользователь добавить план
    dp.message.register(basic.get_project_name_user, add_plan_user.GET_PROJECT_NAME)
    dp.message.register(basic.get_start_time_user, add_plan_user.GET_START_TIME)
    dp.message.register(basic.get_end_time_user, add_plan_user.GET_END_TIME)
    dp.message.register(basic.get_date_user, add_plan_user.GET_DATE)
    # Регистрация добавить план
    dp.message.register(basic.add_fact, F.text == "Добавить факт")

    dp.message.register(basic.get_project_name_fact, add_fact_user.GET_PROJECT_NAME)
    dp.message.register(basic.get_comment_fact, add_fact_user.GET_COMMENT)
    dp.message.register(basic.get_start_time_fact, add_fact_user.GET_START_TIME)
    dp.message.register(basic.get_end_time_fact, add_fact_user.GET_END_TIME)
    dp.message.register(basic.get_date_fact, add_fact_user.GET_DATE)
    # Регистрация нового пользователя
    dp.message.register(admin_handlers.add_new_employer, F.text == "Добавить пользователя")

    dp.message.register(admin_handlers.add_new_employer_id, add_employer.GET_ID)
    dp.message.register(admin_handlers.add_employer_name, add_employer.GET_NAME)
    dp.message.register(admin_handlers.add_employer_surname, add_employer.GET_SURNAME)
    dp.message.register(admin_handlers.add_employer_permission, add_employer.GET_PERMISSION)
    
    # Удаление пользователя
    # ТУТ КОСЯК С ПОИСКОМ ПОЛЬЩОВАТЕЛЯ!!! ПРОВЕРИТЬ ВЕЗДЕ, КОГДА ПОДТЯНУ ПОЛЬЗОВАТЕЛЕЙ И БД
    dp.message.register(admin_handlers.delete_employer, F.text == "Удалить пользователя")
    dp.message.register(admin_handlers.delete_employer_id, delete_employeer.GET_ID)
    # Изменение прав пользователя
    # ТУТ КОСЯК С ПОИСКОМ ПОЛЬЩОВАТЕЛЯ!!! ПРОВЕРИТЬ ВЕЗДЕ, КОГДА ПОДТЯНУ ПОЛЬЗОВАТЕЛЕЙ И БД
    dp.message.register(admin_handlers.edit_employer_permisson, F.text == "Изменить права")
    dp.message.register(admin_handlers.edit_employer_permisson_id, change_permissions.GET_ID)
    dp.message.register(admin_handlers.edit_employer_permisson_permission, change_permissions.GET_PERMISSION)
    # Просмотр плана админ

    # Просмотр плана пользователь

    # Список пользователей

    # Хелп админ

    # Хелп пользователь

    try:
        await dp.start_polling(bot)
    finally:
        bot.session.close()


if __name__ == "__main__":
    asyncio.run(Start())
