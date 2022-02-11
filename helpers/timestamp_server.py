from datetime import datetime
print(datetime.fromtimestamp(int("1644428546382"[:-3])).strftime('%d-%m-%Y %H:%M:%S'))
