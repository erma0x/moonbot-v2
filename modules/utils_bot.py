import requests
from math import floor
from datetime import datetime
from binance.helpers import round_step_size, get_step_size
from binance import  BinanceSocketManager

# async def format_coin_quantity(qnt,symbol):
#     step_size = get_step_size(symbol)
#     formatted_quantity = round_step_size(qnt, step_size) - step_size
#     return formatted_quantity

def timestamp_to_date(time):
    time = str(time)
    return(datetime.fromtimestamp(int(time[:-3])).strftime('%d-%m-%Y %H:%M:%S'))

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


async def get_data(client,token_pair='BNBUSDT'): ############### NON KLINE MA PREZZO SINGOLO
    bm = BinanceSocketManager(client)
    async with bm.kline_socket(symbol=token_pair) as stream:        
        res = await stream.recv()
        #print(' token: ',token_pair,' price: ',res['k']['c'] ,' volume: ',res['k']['V'],'  date: ',timestamp_to_date(res['k']['T']))
        return( float( res['k']['c'] ) ) 

def print_order(order_):
    text ="""

symbol \t\t       {1}

OPEN PRICE \t {5}
original quantity\t{4}

transaction time\t{2}

order ID        \t{0} 
client order ID \t{3}

guadagno assoluto    stimato $ \t{6}
guadagno percentuale stimato % \t{7}
guadagno assoluto    effettivo $ \t{8}
guadagno percentuale effettivo % \t{9}

    """.format(order_['orderId'],
    order_['symbol'],
    order_['side'],
    timestamp_to_date(order_['transactTime']),
    order_['clientOrderId'],
    order_['origQty'],
    order_['price'])
    print(text)