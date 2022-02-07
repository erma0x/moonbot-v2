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


def prendi_i_prezzi(symbol1,symbol2):
    price_usdt = client.get_avg_price(symbol=symbol1) #
    price_busd = client.get_avg_price(symbol=symbol2) #
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
    print('CLIENT PING ',client.ping())

    status = client.get_system_status()
    print('SYSTEM STATUS ',status)
    
    info_snapshot = client.get_account_snapshot(type='SPOT')
    print('SNAPSHOT account ',info_snapshot)

    info_account = client.get_account()
    print('INFO account ',info_account)

    balanceBUSD = client.get_asset_balance(asset='BUSD')  
    balanceUSDT = client.get_asset_balance(asset='USDT')
    print('\nYOUR BALANCE IS -> ',balanceBUSD+balanceUSDT)
    print('BUSD : ',balanceBUSD)
    print('USDT : ',balanceUSDT)

    investimento = 20
    leverage = 1
    guadagno_minimo_assoluto = 1
    guadagno_minimo_percentuale = 0.007 # in %
    my_symbols = ['DAR','BTC','ETH']    #my_symbols = client.get_all_tickers()  

    for i in my_symbols:
        usdtheter,usdbinance = prendi_i_prezzi(i+'USDT',i+'BUSD')

        gain_abs, gain_prc = calcola_guadagno(price_usdt=usdtheter,price_busd=usdbinance,
                                                    capitale=investimento,leva=leverage)

        print('-'*80)
        print('SIMBOLO ',i)
        print('price USD Theter\n',usdtheter['price'],'price USD Binance',usdbinance['price'])
        print('\nguadagno assoluto: ',round(gain_abs,4),'$')
        print('guadagno percentuale :',round(gain_prc,6),'%\n')

        if gain_prc >= guadagno_minimo_percentuale:
            print('\n**** ESEGUO OPERAZIONE ****\n')

            if usdtheter['price'] > usdbinance['price']:
                coin_quantity = investimento/usdbinance['price']
                order = client.order_limit_buy(
                    symbol = i+'BUSD',
                    quantity = coin_quantity,
                    price = usdbinance['price'])

            if usdtheter['price'] < usdbinance['price']:
                coin_quantity = investimento/usdtheter['price']
                order = client.order_limit_buy(
                    symbol=i+'USDT',
                    quantity=coin_quantity,
                    price=usdtheter['price'])

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
