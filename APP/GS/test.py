# gs key 1JED99HzVcXP6HtQJ-vFHibCl1HB8TuESITHG_mL6J98

import calendar
import datetime
import gspread
from gspread.exceptions import APIError


class GoogleSheetsManager:
    def __init__(self, credentials_path, spreadsheet_key):
        self.gc = gspread.service_account(filename=credentials_path)
        self.spreadsheet = self.gc.open_by_key(spreadsheet_key)
        self.worksheet = None
        self.worksheets = self.spreadsheet.worksheets()
        self.times_list = [
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

    def create_sheet(self, title, rows, cols):
        existing_sheet = None
        for sheet in self.worksheets:
            if title == sheet.title:
                existing_sheet = sheet
                break
        if existing_sheet is not None:
            self.worksheet = existing_sheet
            print(f"Selected existing sheet '{title}'.")
        else:
            try:
                self.worksheet = self.spreadsheet.add_worksheet(
                    title=title, rows=rows, cols=cols
                )
                self.worksheets = self.spreadsheet.worksheets()
                print(f"Created new sheet '{title}'.")
            except APIError as e:
                print(f"Error creating sheet: {e}")

    def add_employees(self, employees):
        if self.worksheet is not None:
            self.worksheet.update_cell(1, 1, "Польз/время")
            col = 2
            for employee in employees:
                try:
                    self.worksheet.update_cell(col, 1, employee)
                    col += 1
                except APIError as e:
                    print(f"Error adding employee: {e}")
        else:
            print("No worksheet is selected.")

    def add_dates(self, dates):
        if self.worksheet is not None:
            row = 2
            for date in dates:
                try:
                    self.worksheet.update_cell(1, row, date)
                    row += 1
                except APIError as e:
                    print(f"Error adding date: {e}")
        else:
            print("No worksheet is selected.")

    def add_employee(self, employee_name):
        if self.worksheet is not None:
            col = 1
            while True:
                try:
                    cell_value = self.worksheet.cell(col, 1).value
                    print(cell_value)
                    if (cell_value == None) or (cell_value == employee_name):
                        self.worksheet.update_cell(col, 1, employee_name)
                        break
                    col += 1
                except APIError as e:
                    print(f"Error adding employee: {e}")
                    break
            print(f"Added employee '{employee_name}' to the worksheet.")
        else:
            print("No worksheet is selected.")

    def add_info(self, value, employee_name, ts, te):
        if self.worksheet is not None:
            try:
                row = self.worksheet.find(employee_name).row
                col_st = self.worksheet.find(ts).col
                col_ed = self.worksheet.find(te).col
                for cell in range(col_st, col_ed + 1):
                    self.worksheet.update_cell(row, cell, value)
            except gspread.CellNotFound:
                print(
                    f"Employee '{employee_name}' or timestamps '{ts}' and '{te}' not found."
                )
            except APIError as e:
                print(f"Error adding info: {e}")
        else:
            print("No worksheet is selected.")

    def exist_sheet(self, title):
        existing_sheet = None
        for sheet in self.worksheets:
            if title == sheet.title:
                existing_sheet = sheet
                break
        if existing_sheet is not None:
            self.worksheet = existing_sheet
            return True
        else:
            return False

    def get_values(self, employee_name):
        if self.worksheet is not None:
            try:
                values = []
                row = self.worksheet.find(employee_name).row
                # print(row)
                # print(f'\n\n\n\n\n')
                for col in range(2, 26):
                    value = self.worksheet.cell(row, col).value
                    if value == None:
                        values.append("Ничего")
                    else:
                        values.append(value)
            except APIError as e:
                print(f"Error retrieving values: {e}")
        else:
            print("No worksheet is selected.")

        Result = {self.times_list[i]: values[i] for i in range(0, len(self.times_list))}
        Final = ""
        for key, value in Result.items():
            Final += f"{key} - {value}\n"
        return Final


# ===================================================

credentials_path = "credentials.json"
spreadsheet_key = "1JED99HzVcXP6HtQJ-vFHibCl1HB8TuESITHG_mL6J98"


# gsm = GoogleSheetsManager(credentials_path, spreadsheet_key)
# gsm.create_sheet(f'{datetime.datetime.now().strftime("%d.%m.%Y Plan")}', 30, 25)
# print(gsm.get_values("Юдин Никита"))
# employees = ['John Doe', 'Jane Smith', 'Bob Johnson']
# gsm.add_employees(employees)

dates = ["2022-01-01", "2022-01-02", "2022-01-03"]
# gsm.add_dates(Time_list)
# gsm.add_employee("John Doe")
# gsm.add_info('value', 'John Doe', '0:00', '15:00')


class GoogleSheetsManagerFact:
    def __init__(self, credentials_path, spreadsheet_key):
        self.gc = gspread.service_account(filename=credentials_path)
        self.spreadsheet = self.gc.open_by_key(spreadsheet_key)
        self.worksheet = None
        self.worksheets = self.spreadsheet.worksheets()

    def create_sheet(self, title, rows, cols):
        existing_sheet = None
        for sheet in self.worksheets:
            if title == sheet.title:
                existing_sheet = sheet
                break
        if existing_sheet is not None:
            self.worksheet = existing_sheet
            print(f"Selected existing sheet '{title}'.")
        else:
            try:
                self.worksheet = self.spreadsheet.add_worksheet(
                    title=title, rows=rows, cols=cols
                )
                self.worksheets = self.spreadsheet.worksheets()
                print(f"Created new sheet '{title}'.")
            except APIError as e:
                print(f"Error creating sheet: {e}")

    def add_dates(self, dates):
        if self.worksheet is not None:
            self.worksheet.update_cell(1, 1, 'Проект/дата')
            row = 2
            for date in dates:
                try:
                    self.worksheet.update_cell(1, row, date)
                    row += 1
                except APIError as e:
                    print(f"Error adding date: {e}")
        else:
            print("No worksheet is selected.")

    def add_project(self, project_title):
        if self.worksheet is not None:
            col = 1
            while True:
                try:
                    cell_value = self.worksheet.cell(col, 1).value
                    print(cell_value)
                    if (cell_value == None) or (cell_value == project_title):
                        self.worksheet.update_cell(col, 1, project_title)
                        break
                    col += 1
                except APIError as e:
                    print(f"Error adding employee: {e}")
                    break
            print(f"Added project info '{project_title}' to the worksheet.")
        else:
            print("No worksheet is selected.")

    def add_info(self, value, project_name, date):
        if self.worksheet is not None:
            try:
                row = self.worksheet.find(project_name).row
                col = self.worksheet.find(date).col
                print(f'\n\n\n\n===================================')
                print(row, col)
                print(f'\n\n\n\n===================================')
                self.worksheet.update_cell(row, col, value)
            except gspread.CellNotFound:
                print(f"Employee '{project_name}' or timestamps '{date}'.")
            except APIError as e:
                print(f"Error adding info: {e}")
        else:
            print("No worksheet is selected.")


Fact_sheet_key = '1KadOW7sNEFD291vCrCKJ1l6056MINJGXhM1ccXDGgno'
def get_minth_list(td):
# Получаем текущую дату
    today = td 
# Получаем количество дней в текущем месяце
    _, num_days = calendar.monthrange(today.year, today.month)
# Создаем список чисел текущего месяца
    month_numbers = list(range(1, num_days+1))
    return month_numbers

#print(month_numbers)
#gsmf = GoogleSheetsManagerFact(credentials_path, Fact_sheet_key)
#gsmf.create_sheet(f'{datetime.date.today().month} fact', 30, 33)
#gsmf.add_dates(month_numbers)
#gsmf.add_project('Проект 1')
#gsmf.add_info('Комментарий', 'Проект 1', '5')
# gsm.add_employees(employees)

#dates = ["2022-01-01", "2022-01-02", "2022-01-03"]
# gsm.add_dates(Time_list)
# gsm.add_employee("John Doe")
# gsm.add_info('value', 'John Doe', '0:00', '15:00')