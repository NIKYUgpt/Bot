import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1JED99HzVcXP6HtQJ-vFHibCl1HB8TuESITHG_mL6J98

class GoogleSheets_plan:
    def __init__(self, credentials_file, spreadsheet_name, sheet_name, sheet_id):
        self.credentials_file = credentials_file
        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.sheet = spreadsheet_name
        self.worksheet_name = sheet_name
        self.sheet_id = sheet_id
    
    def authenticate(self):
        gc = gspread.service_account(filename=self.credentials)
        GSheet_fact = gc.open_by_key(self.sheet_id)
        