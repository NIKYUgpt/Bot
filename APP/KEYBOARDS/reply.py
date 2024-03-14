from aiogram import types
from datetime import datetime, timedelta
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType

time_selector = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="0:00"),
            KeyboardButton(text="1:00"),
            KeyboardButton(text="2:00"),
            KeyboardButton(text="3:00"),
            KeyboardButton(text="4:00"),
            KeyboardButton(text="5:00"),
        ],
        [
            KeyboardButton(text="6:00"),
            KeyboardButton(text="7:00"),
            KeyboardButton(text="8:00"),
            KeyboardButton(text="9:00"),
            KeyboardButton(text="10:00"),
            KeyboardButton(text="11:00"),
        ],
        [
            KeyboardButton(text="12:00"),
            KeyboardButton(text="13:00"),
            KeyboardButton(text="14:00"),
            KeyboardButton(text="15:00"),
            KeyboardButton(text="16:00"),
            KeyboardButton(text="17:00"),
        ],
        [
            KeyboardButton(text="18:00"),
            KeyboardButton(text="19:00"),
            KeyboardButton(text="20:00"),
            KeyboardButton(text="21:00"),
            KeyboardButton(text="22:00"),
            KeyboardButton(text="23:00"),
        ],
        [
            KeyboardButton(text="Стоп"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери кнопку",
    selective="True",
)

cancel_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Стоп")]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери кнопку",
    selective="True",
)

date_selector = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="1234")]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери кнопку",
    selective="True",
)

start_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="/start")]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери кнопку",
    selective="True",
)
