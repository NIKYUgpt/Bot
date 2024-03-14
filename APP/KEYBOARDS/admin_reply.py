from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType

admin_reply_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить пользователя"),
            KeyboardButton(text="Удалить пользователя"),
            KeyboardButton(text="Список пользователей"),
        ],
        [
            KeyboardButton(text="Добавить План"),
            KeyboardButton(text="Добавить факт"),
            KeyboardButton(text="Просмотреть план"),
            KeyboardButton(text="Изменить права доспупа пользователя"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери кнопку",
    selective="True",
)
