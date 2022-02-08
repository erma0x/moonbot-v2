from math import ceil, floor
import requests, json

"""
BINANCE - LOT_SIZE ERROR
Function to round the value according to decimal places in Binance.
When placing a purchase order with API you get the LOT_SIZE error.
To avoid the error you must round the decimal places according to the 'stepSize' of each coin.
"""
from pprint import pprint



def format_coin_quantity(initial_coin_quantity, symbol = 'ETHUSDT',direction = floor):
    URL = "https://www.binance.com/api/v3/exchangeInfo?symbols=[%22" + str(symbol) + "%22]"
    result = requests.get(URL).json()
    print('RISULTATI ',result)

    numbers_after_zero = result['symbols'][0]['filters'][2]['stepSize']
    print('NUMERI DOPO LO ZERO ',numbers_after_zero)

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


value = format_coin_quantity( 324.214218462874612,symbol='BTCUSDT' )

print('value ',value)