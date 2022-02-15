#!/usr/bin/env python3.7
# coding: utf-8
"""
in the shell 
export binance_api="your_api_key_here"
export binance_secret="your_api_secret_here"
"""
import imp
import os
import asyncio
from binance.enums import *
from binance import AsyncClient
from copy import deepcopy
from modules.utils_bot import *
import time

async def main():
    """
    guadagno_assoluto_effettivo = float(SELL_open_orders[i]['origQty'])*(float(SELL_open_orders[i]['price'])-float(prezzo_di_apertura))
    guadagno_percentuale_effettivo = guadagno_assoluto_effettivo/investimento*100
    """
    api_key = os.environ.get('binance_api') 
    api_secret = os.environ.get('binance_secret')
    client = await AsyncClient.create(api_key, api_secret)

    investimento = 40 # $
    prezzo_di_apertura = 0 
    minimo_guadagno_assoluto = 1 # $
    minimo_guadagno_percentuale = 0.09 # %[0,100]
    
    numero_massimo_ordini = 1
    my_symbol = 'QI'

    BUY_open_orders = []
    SELL_open_orders = []
    FILLED_orders = []

    while True:
        priceUSDT = await get_data(client,token_pair=my_symbol+'BUSD')
        priceBUSD = await get_data(client,token_pair=my_symbol+'USDT')
        print(my_symbol+'USDT ',priceUSDT,'\t|\t',my_symbol+'BUSD : ',priceBUSD)
        
        lower_price_stablecoin = min(priceUSDT,priceBUSD)
        coin_quantity = investimento/lower_price_stablecoin
        guadagno_assoluto_stimato = investimento/min(priceUSDT,priceBUSD)*max(priceUSDT,priceBUSD) - investimento
        guadagno_percentuale_stimato = guadagno_assoluto_stimato/investimento*100
        print('guadagno stimato: % ',guadagno_percentuale_stimato,': $ ',guadagno_assoluto_stimato)
# BUY TOKEN  
        if guadagno_percentuale_stimato >= minimo_guadagno_percentuale and numero_massimo_ordini>len(BUY_open_orders):
            if priceUSDT > priceBUSD:
                buy_stablecoin='BUSD'

            if priceUSDT < priceBUSD:
                buy_stablecoin='USDT'

            buy_symbol = my_symbol+buy_stablecoin 
            order = await client.create_order(
                    symbol=buy_symbol,
                    side=client.SIDE_BUY,
                    type=client.ORDER_TYPE_MARKET,
                    quantity = await format_coin_quantity(coin_quantity, symbol = buy_symbol))

            print_OPEN(order)
            BUY_open_orders.append(order)

# SELL TOKEN 
        time.sleep(1)
        if len(BUY_open_orders)>0:
            sell_priceUSDT = await get_data(client,token_pair=my_symbol+'USDT')
            sell_priceBUSD = await get_data(client,token_pair=my_symbol+'BUSD')
            print('SELLING : ',my_symbol+'USDT ',sell_priceUSDT,'\t|\t',my_symbol+'BUSD : ',sell_priceBUSD)
        
            if sell_priceUSDT < sell_priceBUSD:
                sell_stablecoin='BUSD'

            if sell_priceUSDT > sell_priceBUSD:
                sell_stablecoin='USDT'

            for i in range(len(BUY_open_orders)):
                if BUY_open_orders[i]['status']=='FILLED':
                    
                    sell_symbol = deepcopy(my_symbol+sell_stablecoin)
                    # order = await client.create_sell_limit(
                    #     symbol=sell_symbol,
                    #     side=client.SIDE_SELL,
                    #     type=client.ORDER_TYPE_MARKET,
                    #     quantity=await format_coin_quantity(coin_quantity, symbol = my_symbol+sell_stablecoin))

                    order = await client.order_limit_sell(timeInForce='GTC',
                                        symbol = sell_symbol,
                                        quantity = await format_coin_quantity(coin_quantity,symbol=sell_symbol),
                                        price = round(float(max(sell_priceUSDT,sell_priceBUSD)),2)) # round 2, or 4


                    print_OPEN(order)
                    print_FILLED(order)

                    SELL_open_orders.append(order)
                    #FILLED_orders.append(BUY_open_orders[i])
                    BUY_open_orders.remove(BUY_open_orders[i])

        if len(SELL_open_orders)>0:
            for i in range(len(SELL_open_orders)):
                if SELL_open_orders[i]['status']=='FILLED':
                    #FILLED_orders.append(SELL_open_orders[i])
                    print_FILLED(SELL_open_orders[i])
                    SELL_open_orders.remove(SELL_open_orders[i])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())