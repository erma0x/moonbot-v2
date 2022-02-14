#!/usr/bin/env python3.7
# coding: utf-8
"""
in the shell ...
export binance_api="your_api_key_here"
export binance_secret="your_api_secret_here"
"""
import os
import requests
import asyncio
import asyncio
from datetime import datetime
from math import floor
#from binance.enums import *
from binance import AsyncClient, BinanceSocketManager

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

def timestamp_to_date(time):
    time=str(time)
    return(datetime.fromtimestamp(int(time[:-3])).strftime('%d-%m-%Y %H:%M:%S'))

async def get_data(client,token_pair='BNBUSDT'):
    bm = BinanceSocketManager(client)
    async with bm.kline_socket(symbol=token_pair) as stream:        
        res = await stream.recv()
        print('date: ',timestamp_to_date(res['k']['T']))
        #print('date: ',timestamp_to_date(res['k']['T']), ' closing price: ',res['k']['c'] , ' volume: ',res['k']['V'])
        return(res['k']['c']) 

async def main():
    """
    order object example
    {'symbol': 'ETHBUSD', 'orderId': 7760933105, 'orderListId': -1, 
    'clientOrderId': 'RKPcQ9jAOT8LlUYK3xygGB', 'transactTime': 1644342622758, 
    'price': '3040.28000000', 'origQty': '0.00490000', 'executedQty': '0.00000000', 
    'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC',
    'type': 'LIMIT', 'side': 'BUY', 'fills': []}
    """
    open_BUY_orders = []
    open_SELL_orders = []

    api_key = os.environ.get('binance_api') 
    api_secret = os.environ.get('binance_secret')
    client = await AsyncClient.create(api_key, api_secret)

    investimento = 20 # $

    minimo_guadagno_assoluto = 1 # $
    minimo_guadagno_percentuale = 0.02 # %[0,100]

    numero_massimo_ordini = 1
    symbol = 'ETH'

    while True:
        dataUSDT = await get_data(client,token_pair=symbol+'BUSD')
        dataBUSD = await get_data(client,token_pair=symbol+'USDT')
        priceUSDT = float(dataUSDT)
        priceBUSD = float(dataBUSD)
        #print(symbol+'USDT : ',priceUSDT,'\t',symbol+'BUSD : ',priceBUSD)
        lower_price_stablecoin = min(priceUSDT,priceBUSD)
        coin_quantity = investimento/lower_price_stablecoin
        guadagno_assoluto_stimato = investimento/min(priceUSDT,priceBUSD)*max(priceUSDT,priceBUSD) - investimento
        guadagno_percentuale_stimato = guadagno_assoluto_stimato/investimento*100
        #print('guadagno stimato $ ',guadagno_assoluto)
        
        if guadagno_percentuale_stimato >= minimo_guadagno_percentuale and numero_massimo_ordini>len(open_BUY_orders):
            if priceUSDT > priceBUSD:
                stablecoin='BUSD'

            if priceUSDT < priceBUSD:
                stablecoin='USDT'

            order = await client.order_limit_buy(timeInForce='GTC',
                                symbol = symbol+stablecoin,
                                quantity = await format_coin_quantity(coin_quantity),
                                price = round(float(lower_price_stablecoin),4)) # round 2, or 4
                
            testo ="""
SEGNALE DI ENTRATA 
APRO L'ORDINE DI ACQUISTO DEL TOKEN
    order ID        \t{0} 
    symbol \t\t       {1}
    transaction time\t{2}
    client order ID \t{3}
    original quantity\t{4}

    guadagno assoluto stimato $ \t{5}
    guadagno percentuale stimato % \t{6}

            """.format(order['orderId'],
            order['symbol'],
            timestamp_to_date(order['transactTime']),
            order['clientOrderId'],
            order['origQty'],
            guadagno_assoluto_stimato,
            guadagno_percentuale_stimato)
            print(testo)
            prezzo_di_apertura = order['price']
            open_BUY_orders.append(order)
##########################################################################
        if len(open_BUY_orders)>0:
            if max(priceUSDT,priceBUSD) == priceUSDT:
                sell_stablecoin='USDT' 

            if max(priceUSDT,priceBUSD) == priceBUSD:
                sell_stablecoin='BUSD'

            for i in range(len(open_BUY_orders)):
                my_order = open_BUY_orders[i]
                print(my_order)
                print(" DEBUGGURE QUI")
                if my_order['status']=='FILLED': ####################
                    order = await client.order_limit_sell(timeInForce='GTC',
                        symbol = symbol+sell_stablecoin,
                        quantity = my_order['origQty'],
                        price = round(max(priceUSDT,priceBUSD),4))

                    testo ="""
ORDINE DI ACQUISTO DEL TOKEN RIUSCITO
APRO L'ORDINE DI VENDITA DEL TOKEN

    order ID        \t{0} 
    symbol \t\t       {1}
    transaction time\t{2}
    client order ID \t{3}
    executed quantity\t{4}

    guadagno assoluto stimato $ \t{5}
    guadagno percentuale stimato % \t{6}
                            """.format(my_order['orderId'],
                            my_order['symbol'],
                            timestamp_to_date(my_order['transactTime']),
                            my_order['clientOrderId'],
                            my_order['origQty'],
                            guadagno_assoluto_stimato,
                            guadagno_percentuale_stimato)
                    print(testo)
                    open_SELL_orders.append(order)
                    open_BUY_orders.remove(open_BUY_orders[i])

        if len(open_SELL_orders)>0:
            for i in range(len(open_SELL_orders)):
                my_order = open_SELL_orders[i]
                if my_order['status']=='FILLED':
                    
                    guadagno_assoluto_effettivo = float(my_order['origQty'])*(float(my_order['price'])-float(prezzo_di_apertura))
                    guadagno_percentuale_effettivo = guadagno_assoluto_effettivo/investimento*100

                    testo="""
VENDITA DEL TOKEN RIUSCITA
CALCOLO GUADAGNO EFFETTIVO

    order ID        \t{0} 
    symbol \t\t       {1}
    transaction time\t{2}
    client order ID \t{3}
    executed quantity\t{4}

    guadagno assoluto stimato $ \t{5}
    guadagno percentuale stimato % \t{6}
    
    guadagno assoluto effettivo $\t {7}
    guadagno percentuale effettivo %\t {8}
                            """.format(my_order['orderId'],
                            my_order['symbol'],
                            timestamp_to_date(my_order['transactTime']),
                            my_order['clientOrderId'],
                            my_order['origQty'],
                            guadagno_assoluto_stimato,
                            guadagno_percentuale_stimato,
                            guadagno_assoluto_effettivo,
                            guadagno_percentuale_effettivo)
                    print(testo)
                    print(' ',open_SELL_orders[i])
                    open_SELL_orders.remove(open_SELL_orders[i])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
