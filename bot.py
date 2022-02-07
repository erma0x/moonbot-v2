#!/usr/bin/env python3.7
# coding: utf-8
"""
in the shell ...
export binance_api="your_api_key_here"
export binance_secret="your_api_secret_here"
"""
from http import client
import os
import urllib 
import http
import requests
import asyncio

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
       
def main():
    """puoi giocare sul guadagno minimo assoluto o percentuale"""
    
    api_key = os.environ.get('binance_api')
    api_secret = os.environ.get('binance_secret')
    
    client = Client(api_key, api_secret)  
    status = client.get_system_status()

    print('system status  (default = normal)   :',status['msg'].upper())
    
    print('*price test ETH-USDT*',client.get_avg_price(symbol='ETHUSDT'))

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
    minimo_guadagno_percentuale = 0.07 # in %

    my_symbols = ['DAR','BTC','ETH']    #my_symbols = client.get_all_tickers()  

    for i in my_symbols:
        usdtheter,usdbinance = prendi_i_prezzi(cliente=client,symbol1=i+'USDT',symbol2=i+'BUSD')

        guadagno_assoluto, guadagno_percentuale = calcola_guadagno(price_usdt=usdtheter,price_busd=usdbinance,
                                                    capitale=investimento,leva=leverage)

        print()
        print('-'*80+'\nsimbolo: ',i)
        print('\nprezzo in Theter (USDT) \t: ',usdtheter['price'],'\nprezzo in binance USD (BUSD) \t: ',usdbinance['price'])
        print('\nguadagno assoluto\t: ',round(guadagno_assoluto,5),'$')
        print('guadagno percentuale\t:',round(guadagno_percentuale,7),'%\n')

        busd_info = client.get_symbol_info(i+'USDT')
        usdt_info = client.get_symbol_info(i+'BUSD')
        busd_min_quantity = busd_info['filters'][2]['minQty']
        usdt_min_quantity = usdt_info['filters'][2]['minQty']
        if guadagno_percentuale >= minimo_guadagno_percentuale:
            print('\n**** ESEGUO OPERAZIONE ****\n')

            if usdtheter['price'] > usdbinance['price']:
                coin_quantity = investimento/float(usdbinance['price'])
                order = client.order_limit_buy(
                    symbol = i+'BUSD',
                    quantity = busd_min_quantity,
                    price = round(float(usdbinance['price']),2))

            if usdtheter['price'] < usdbinance['price']:
                coin_quantity = investimento/float(usdtheter['price'])
                order = client.order_limit_buy(
                    symbol=i+'USDT',
                    quantity=usdt_min_quantity,
                    price=round(float(usdtheter['price']),2))
            
            if order:
                print(order)

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
