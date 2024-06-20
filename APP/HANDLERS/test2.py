

from datetime import datetime, timedelta


today = datetime.today().date()
allowed_dates = [(today + timedelta(days=i)).strftime('%d.%m.%Y') for i in range(7)]

print(today)
print(allowed_dates)