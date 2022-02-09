from datetime import datetime
print(datetime.fromtimestamp(int("1644427778926"[:-3])).strftime('%d-%m-%Y %H:%M:%S'))
