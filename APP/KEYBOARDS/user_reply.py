from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType

user_reply_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить План"),
            KeyboardButton(text="Добавить факт"),
            KeyboardButton(text="Список пользователей"),
        ],
        [
            KeyboardButton(text="Просмотреть план"),
            KeyboardButton(text="Помощь"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери кнопку",
    selective="True",
)
