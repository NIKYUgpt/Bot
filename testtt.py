from APP.GS.test import GoogleSheetsManager
from APP.UTILS.db_commands import UserDatabase
import asyncio

credentials_path = 'credentials.json'
spreadsheet_key = '1JED99HzVcXP6HtQJ-vFHibCl1HB8TuESITHG_mL6J98'
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


async def init1():
    gsm = GoogleSheetsManager(credentials_path, spreadsheet_key)
    gsm.create_sheet('Employees', 100, 20)

    #employees = ['John Doe', 'Jane Smith', 'Bob Johnson']
    database = UserDatabase("users.db")
    employees = await database.users_list_sheet()
    print(employees)
    print('=============================================')
    gsm.add_employees(employees)

    #dates = ['2022-01-01', '2022-01-02', '2022-01-03']
    gsm.add_dates(Time_list)

if __name__ == "__main__":
    mw = init1()

    
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)