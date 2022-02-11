from datetime import datetime
print(datetime.fromtimestamp(int("1644599819999"[:-3])).strftime('%d-%m-%Y %H:%M:%S'))
