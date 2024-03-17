import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheets_plan:
    def __init__(self, credentials_file, spreadsheet_name, sheet_name):
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.sheet_name = sheet_name
        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = None
        self.client = None
        self.sheet = None

    def authenticate(self):
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(self.spreadsheet_name).worksheet(self.sheet_name)

    def add_employers(self, ):
        self.authenticate()
        #Тут подвязать бд и заполнение таблицы по вертикали

    def
