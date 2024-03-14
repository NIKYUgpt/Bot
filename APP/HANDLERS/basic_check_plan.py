from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


from APP.UTILS.db_commands import UserDatabase

from APP.KEYBOARDS.admin_reply import admin_reply_start
from APP.KEYBOARDS.user_reply import user_reply_start
from APP.KEYBOARDS.reply import (
    time_selector,
    cancel_button,
    date_selector,
    start_button,
)


async def check_plan(message: Message, state: FSMContext):
    database = UserDatabase("users.db")
    # ПОХУЙ
    if await database.search_user_by_id(message.from_user.id) == 0:
        await message.answer(
            f"<b>Привет, пользователь</b>\n Вы не зарегистрированны. Прошу обратитесь к менеджеру"
        )
    elif await database.search_user_by_id(message.from_user.id) == 1:
        await message.answer(f"Введите название проекта", reply_markup=user_reply_start)
        id = message.from_user.id
        ful_name = функция
    # Если админ
    elif await database.search_user_by_id(message.from_user.id) >= 2:
        await message.answer(
            f"Заполнение плана пользователю. \n Введите id телеграма пользователя.\n Просмотреть список пользователей можно с помощь команды.",
            reply_markup=cancel_button,
        )
        # Написать стейт для выбора пользователя
        # СТЕЙТ СОСТОИТ ИЗ ОДНОГО ПАРАМЕТРА. id Пользователя
        await state.set_state(ТУТ_СТЕЙТ.GET_ID)