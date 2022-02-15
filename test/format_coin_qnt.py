import requests
from math import floor

async def format_coin_quantity(initial_coin_quantity, symbol = 'ETHUSDT',direction = floor):
    URL = "https://www.binance.com/api/v3/exchangeInfo?symbols=[%22" + str(symbol) + "%22]"
    result = requests.get(URL).json()
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