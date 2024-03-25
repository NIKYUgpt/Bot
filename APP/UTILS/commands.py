import datetime
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
import re

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="help", description="Помощь"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


def check_date_format(date_str):
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    if re.match(pattern, date_str):
        return True
    else:
        return False