from math import ceil, floor
import requests, json
"""
BINANCE - LOT_SIZE ERROR
Function to round the value according to decimal places in Binance.
When placing a purchase order with API you get the LOT_SIZE error.
To avoid the error you must round the decimal places according to the 'stepSize' of each coin.
"""
symbol = 'ETHUSDT'
URL = "https://www.binance.com/api/v3/exchangeInfo?symbols=[%22" + str(symbol) + "%22]"
result = requests.get(URL).json()


def fn_round(num, stepSize, direction = floor):
    zeros = 0
    number = float(stepSize)
    while number < 0.1:
        number *= 10
        zeros += 1
    if float(stepSize) > 0.1:
        places = zeros
    else:
        places = zeros + 1
    return direction(num * (10**places)) / float(10**places)

value = fn_round(324.92839238092803, result['symbols'][0]['filters'][2]['stepSize'])

print(value)
## output: 324.983
