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


def calcola_guadagno(price_usdt,price_busd,capitale=20,leva=1):
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
    
    print('*price test*',client.get_avg_price(symbol='ETHUSDT'))

    # info_snapshot = client.get_account_snapshot(type='SPOT')
    # print('snapshot account ',info_snapshot)

    # info_account = client.get_account()
    # print('INFO account ',info_account)

    asset_balance = client.get_asset_balance(asset='USDT')
    print(asset_balance)
    # for asset in asset_balance['balances']:
    #     if asset['free']>5:
    #         print('\n {0} balance is: {1} coins '.format(asset['asset'],asset['free']))
    
    
    # investimento = 50
    # leverage = 1
    # minimo_guadagno_assoluto = 1
    # minimo_guadagno_percentuale = 0.07 # in %

    # my_symbols = ['DAR','BTC','ETH']    #my_symbols = client.get_all_tickers()  

    # for i in my_symbols:
    #     usdtheter,usdbinance = prendi_i_prezzi(cliente=client,symbol1=i+'USDT',symbol2=i+'BUSD')

    #     guadagno_assoluto, guadagno_percentuale = calcola_guadagno(price_usdt=usdtheter,price_busd=usdbinance,
    #                                                 capitale=investimento,leva=leverage)

    #     print('-'*80)
    #     print('simbolo: ',i)
    #     print('\nprezzo in Theter (USDT) : ',usdtheter['price'],'\nprezzo in binance USD (BUSD) : ',usdbinance['price'])
    #     print('\nguadagno assoluto: ',round(guadagno_assoluto,5),'$')
    #     print('guadagno percentuale :',round(guadagno_percentuale,7),'%\n')

    #     if guadagno_percentuale >= minimo_guadagno_percentuale:
    #         print('\n**** ESEGUO OPERAZIONE ****\n')

            # if usdtheter['price'] > usdbinance['price']:
            #     coin_quantity = investimento/usdbinance['price']
            #     order = client.order_limit_buy(
            #         symbol = i+'BUSD',
            #         quantity = coin_quantity,
            #         price = usdbinance['price'])

            # if usdtheter['price'] < usdbinance['price']:
            #     coin_quantity = investimento/usdtheter['price']
            #     order = client.order_limit_buy(
            #         symbol=i+'USDT',
            #         quantity=coin_quantity,
            #         price=usdtheter['price'])

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
