from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(bots=Bots(bot_token=env.str("TOKEN"), admin_id=env.int("ADMIN_ID")))


settings = get_settings("config")
print(settings)

Time_list = [
    "0:00",
    "1:00",
    "2:00",
    "3:00",
    "4:00",
    "5:00",
    "6:00",
    "7:00",
    "8:00",
    "9:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00",
    "22:00",
    "23:00",
]

Date_list = ["20.03.2024", "21.03.2024"]
credentials_file = 'credentials.json'
Plan_sheet_key = '1JED99HzVcXP6HtQJ-vFHibCl1HB8TuESITHG_mL6J98'