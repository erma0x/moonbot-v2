#!/usr/bin/env python3.7
# coding: utf-8
"""
in the shell ...
export binance_api="your_api_key_here"
export binance_secret="your_api_secret_here"
"""
from math import ceil, floor
import requests
import json
import asyncio
from re import T
import datetime
from http import client
import os
from unicodedata import decimal
import urllib 
import http
import asyncio
import time
import datetime

from binance.enums import *
from binance import AsyncClient, BinanceSocketManager

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

async def get_balance(client):
    USDT_balance = await client.get_asset_balance(asset='USDT')
    BUSD_balance = await client.get_asset_balance(asset='BUSD')
    print('YOUR BALANCE in: \n- USDT balance : ',USDT_balance['free'],'\n- BUSD balance : ',BUSD_balance['free'])
    return USDT_balance, BUSD_balance

async def test_connection(client):
    status = await client.get_system_status()
    print('system status  (default = normal)\t:',status['msg'].upper())
    print('price 5 min ago of ETH-USDT \t\t',client.get_avg_price(symbol='ETHUSDT'))

async def test_stream_data(client):
    bm = BinanceSocketManager(client)
    async with bm.kline_socket(symbol='BNBBTC') as stream:
        while True:
            res = await stream.recv()
            print('date: ',timestamp_to_datetime(res['k']['T']), ' closing price: ',res['k']['c'] , ' volume: ',res['k']['V'])

async def get_stream_data(binanceSocketManager):
    async with binanceSocketManager.kline_socket(symbol=symbol+'USDT') as stream:
        while True:
            res = await stream.recv()
            print('symbol: ',res['s'],' date: ',timestamp_to_datetime(res['k']['T']), ' closing price: ',res['k']['c'] , ' volume: ',res['k']['V'])
            

async def main():    
    api_key = os.environ.get('binance_api')
    api_secret = os.environ.get('binance_secret')
    client = await AsyncClient.create(api_key, api_secret)     
    bm = BinanceSocketManager(client)
    get_stream_data(bm)
    investimento = 15
    leverage = 1
    minimo_guadagno_assoluto = 1
    percentuale_minimo_guadagno = 0.002     
    open_orders = []
    numero_massimo_ordini = 2
    my_symbols = ['ETH','BTC']  

    for symbol in my_symbols:
        print(symbol)

                # guadagno_assoluto = abs(usdtheter-usdbinance) * investimento * leverage
                # guadagno_percentuale = guadagno_assoluto/investimento
                
                # print('date: ',timestamp_to_datetime(res['k']['T']), ' closing price: ',res['k']['c'] , ' volume: ',res['k']['V'])

                # print('-'*80+'\nsimbolo: ',symbol)
                # print('\nPREZZO in Theter \tUSDT \t: ',usdtheter['price'],'\nprezzo in binance USD\tBUSD \t: ',usdbinance['price'])
                # print('\nguadagno ASSOLUTO\t: ',round(guadagno_assoluto,5),'$')
                # print('\nguadagno PERCENTUALE\t: ',round(guadagno_percentuale,7),'%\n')

                # busd_info = client.get_symbol_info(symbol+'USDT')
                # usdt_info = client.get_symbol_info(symbol+'BUSD')
                # busd_min_quantity = busd_info['filters'][2]['minQty']
                # usdt_min_quantity = usdt_info['filters'][2]['minQty']
                
                # print('QUANTITA MINIME ', busd_min_quantity,usdt_min_quantity)
        
                # if len(open_orders) < numero_massimo_ordini:
                #     if float(guadagno_percentuale) >= percentuale_minimo_guadagno:
                #         print('\n**** APRO OPERAZIONE ****\n')

                #         if usdtheter['price'] > usdbinance['price']:
                #             print('eseguo operazione con BUSD')
                #             coin_quantity = investimento/float(usdbinance['price'])
                #             order = client.order_limit_buy(timeInForce='GTC',
                #                 symbol = symbol+'BUSD',
                #                 quantity = format_coin_quantity(coin_quantity),
                #                 price = round(float(usdbinance['price']),2))

                #         if usdtheter['price'] < usdbinance['price']:
                #             print('eseguo operazione con USDT')
                #             coin_quantity = investimento/float(usdtheter['price'])
                #             order = client.order_limit_buy(timeInForce='GTC',
                #                 symbol=i+'USDT',
                #                 quantity = format_coin_quantity(coin_quantity),
                #                 price=round(float(usdtheter['price']),2))

                #         open_orders.append(order)
                
                #     if my_order['executedQty'] == my_order['origQty']: # SE GLI ORDINI SONO STATI FILLATI 
                #         if 'USDT' in my_order['symbol'] :
                #             coin_quantity = investimento/float(usdtheter['price'])
                #             order = client.order_limit_sell(timeInForce='GTC',
                #                 symbol=i+'BUSD',
                #                 quantity = format_coin_quantity(coin_quantity),
                #                 price=round(float(usdbinance['price']),2))

                #         if 'BUSD' in my_order['symbol'] :
                #             coin_quantity = investimento/float(usdtheter['price'])
                #             order = client.order_limit_sell(timeInForce='GTC',
                #                 symbol=symbol+'USDT',
                #                 quantity = format_coin_quantity(coin_quantity),
                #                 price=round(float(usdtheter['price']),2))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
