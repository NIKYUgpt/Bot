from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType # type: ignore

user_reply_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить План"),
            KeyboardButton(text="Добавить факт"),
            KeyboardButton(text="Список пользователей"),
        ],
        [
            KeyboardButton(text="Просмотреть план")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери кнопку",
    selective="True",
)
