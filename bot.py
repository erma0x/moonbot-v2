#!/usr/bin/env python3.7
# coding: utf-8
"""
in the shell ...
export binance_api="your_api_key_here"
export binance_secret="your_api_secret_here"
"""
from math import ceil, floor
import requests, json

from http import client
import os
from unicodedata import decimal
import urllib 
import http
import asyncio
import time

from binance.client import Client
from binance.enums import *

def prendi_i_prezzi(cliente,symbol1,symbol2):
    price_usdt = cliente.get_avg_price(symbol=symbol1) #
    price_busd = cliente.get_avg_price(symbol=symbol2) #
    return(price_usdt,price_busd)


def calcola_guadagno(price_usdt,price_busd,capitale=15,leva=1):
    a ,b =float(price_usdt['price']), float(price_busd['price'])
    differenza_percentuale = abs(a-b)/max(a,b)
    guadagno_assoluto = differenza_percentuale * capitale * leva 
    guadagno_percentuale = guadagno_assoluto/capitale * 100
    return(guadagno_assoluto,guadagno_percentuale)


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



def main():
    """puoi giocare sul guadagno minimo assoluto o percentuale"""
    
    api_key = os.environ.get('binance_api')
    api_secret = os.environ.get('binance_secret')
    
    client = Client(api_key, api_secret) 

    status = client.get_system_status()

    print('system status  (default = normal)\t:',status['msg'].upper())
    print('price test ETH-USDT \t\t',client.get_avg_price(symbol='ETHUSDT'))
    
    
    # info_snapshot = client.get_account_snapshot(type='SPOT')
    # print('snapshot account ',info_snapshot)

    # info_account = client.get_account()
    # print('INFO account ',info_account)

    USDT_balance = client.get_asset_balance(asset='USDT')
    BUSD_balance = client.get_asset_balance(asset='BUSD')

    print('USDT balance : ',USDT_balance['free'],'\nBUSD balance : ',BUSD_balance['free'])
    
    investimento = 15
    leverage = 1
    minimo_guadagno_assoluto = 1
    minimo_guadagno_percentuale = 0.02 # in %
    open_orders = []
    my_symbols = ['ETH']    #my_symbols = client.get_all_tickers()   

    for i in my_symbols:
        usdtheter,usdbinance = prendi_i_prezzi(cliente=client,symbol1=i+'USDT',symbol2=i+'BUSD')

        guadagno_assoluto, guadagno_percentuale = calcola_guadagno(price_usdt=usdtheter,price_busd=usdbinance,
                                                    capitale=investimento,leva=leverage)

        print('-'*80+'\nsimbolo: ',i)
        print('\nPREZZO in Theter \tUSDT \t: ',usdtheter['price'],'\nprezzo in binance USD\tBUSD \t: ',usdbinance['price'])
        print('\nguadagno ASSOLUTO\t: ',round(guadagno_assoluto,5),'$')
        print('\nguadagno PERCENTUALE\t: ',round(guadagno_percentuale,7),'%\n')

        busd_info = client.get_symbol_info(i+'USDT')
        usdt_info = client.get_symbol_info(i+'BUSD')
        busd_min_quantity = busd_info['filters'][2]['minQty']
        usdt_min_quantity = usdt_info['filters'][2]['minQty']
        
        print('QUANTITA MINIME ', busd_min_quantity,usdt_min_quantity)
        numero_massimo_ordini = 2
        for numero_ordine in range(numero_massimo_ordini):
            if float(guadagno_percentuale) >= minimo_guadagno_percentuale:
                print('\n**** APRO OPERAZIONE ****\n')

                if usdtheter['price'] > usdbinance['price']:
                    print('eseguo operazione con BUSD')
                    coin_quantity = investimento/float(usdbinance['price'])
                    order = client.order_limit_buy(timeInForce='GTC',
                        symbol = i+'BUSD',
                        quantity = format_coin_quantity(coin_quantity),
                        price = round(float(usdbinance['price']),2))


                if usdtheter['price'] < usdbinance['price']:
                    print('eseguo operazione con USDT')
                    coin_quantity = investimento/float(usdtheter['price'])
                    order = client.order_limit_buy(timeInForce='GTC',
                        symbol=i+'USDT',
                        quantity = format_coin_quantity(coin_quantity),
                        price=round(float(usdtheter['price']),2))

                open_orders.append(order)
                    #'origQty': '0.00490000', 'executedQty': '0.00000000'
        
        time.sleep(1)
        for my_order in open_orders:
            if my_order['executedQty'] == my_order['origQty']: # SE GLI ORDINI SONO STATI FILLATI 

                if 'USDT' in my_order['symbol'] :
                    coin_quantity = investimento/float(usdtheter['price'])
                    order = client.order_limit_sell(timeInForce='GTC',
                        symbol=i+'BUSD',
                        quantity = format_coin_quantity(coin_quantity),
                        price=round(float(usdbinance['price']),2))

                if 'BUSD' in my_order['symbol'] :
                    coin_quantity = investimento/float(usdtheter['price'])
                    order = client.order_limit_sell(timeInForce='GTC',
                        symbol=i+'USDT',
                        quantity = format_coin_quantity(coin_quantity),
                        price=round(float(usdtheter['price']),2))


if __name__ == "__main__":   
    main()

# async def main():
#     api_key = os.environ.get('binance_api')
#     api_secret = os.environ.get('binance_secret')
#     client = await AsyncClient.create(api_key, api_secret)   
#     #doge_busd = client.get_symbol_ticker(symbol="DOGEBUSD")
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
