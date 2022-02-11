import requests
from datetime import datetime
from math import floor

async def format_coin_quantity(initial_coin_quantity, symbol = 'ETHUSDT',direction = floor):
    URL = "https://www.binance.com/api/v3/exchangeInfo?symbols=[%22" + str(symbol) + "%22]"
    result = await requests.get(URL).json()
    numbers_after_zero = result['symbols'][0]['filters'][2]['stepSize']
    zeros = 0
    number = float(numbers_after_zero)
    while number < 0.1:
        number *= 10
        zeros += 1
    if float(numbers_after_zero) > 0.1:
        places = zeros
    else:
        places = zeros + 1
    return direction(initial_coin_quantity * (10**places)) / float(10**places)

def timestamp_to_datetime(time):
    time=str(time)
    return(datetime.fromtimestamp(int(time[:-3])).strftime('%d-%m-%Y %H:%M:%S'))

print(timestamp_to_datetime('1644599819999'))