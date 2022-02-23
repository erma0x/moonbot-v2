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
    guadagno_assoluto_effettivo = float(orderbookSELL[i]['origQty'])*(float(orderbookSELL[i]['price'])-float(prezzo_di_apertura))
    guadagno_percentuale_effettivo = guadagno_assoluto_effettivo/investimento*100
    """
    api_key = os.environ.get('binance_api') 
    api_secret = os.environ.get('binance_secret')
    client = await AsyncClient.create(api_key, api_secret)


    commissioniSpotMaker = 0.075 # %
    commissioniSpotTaker = 0.075 # %

    investimento = 12 # $
    prezzo_di_apertura = 0 
    minimo_guadagno_assoluto = 1 # $
    minimo_guadagno_percentuale_buy = 0.09 # %[0,100]
    minimo_guadagno_percentuale_sell = 0.1 # %[0,100]

    numero_massimo_ordini = 1
    my_symbol = 'ETH'

    orderbookBUY = []
    orderbookSELL = []
    FILLED_orders = []

    while True:
        priceBUSD = await get_data(client,token_pair=my_symbol+'BUSD')
        priceUSDT = await get_data(client,token_pair=my_symbol+'USDT')
        
        print(my_symbol+'USDT ',priceUSDT,'\t|\t',my_symbol+'BUSD : ',priceBUSD)
        
        lower_price_stablecoin = min(priceUSDT,priceBUSD)
        coin_quantity = investimento/lower_price_stablecoin
        guadagno_assoluto_stimato = coin_quantity*max(priceUSDT,priceBUSD) - investimento
        guadagno_percentuale_stimato = guadagno_assoluto_stimato/investimento*100
        
        print('guadagno stimato: % ',guadagno_percentuale_stimato,': $ ',guadagno_assoluto_stimato)

# BUY TOKEN  
        if guadagno_percentuale_stimato+commissioniSpotMaker >= minimo_guadagno_percentuale_buy and numero_massimo_ordini>=len(orderbookBUY):
            if priceUSDT > priceBUSD:
                buy_stablecoin='BUSD'

            if priceUSDT < priceBUSD:
                buy_stablecoin='USDT'

            buy_symbol = my_symbol + buy_stablecoin


            order = await client.order_limit_buy(timeInForce='GTC',
                                symbol = buy_symbol,
                                quantity = await format_coin_quantity(coin_quantity, symbol = buy_symbol),
                                price = round(float(min(priceBUSD,priceUSDT)),2))


            order['prezzo_di_apertura_buy'] = min(priceBUSD,priceUSDT)
            print_OPEN(order)
            orderbookBUY.append(order)

# SELL TOKEN 
        if len(orderbookBUY)>0:
            for i in range(len(orderbookBUY)):

                if orderbookBUY[i]['status']=='FILLED':

                    priceUSDT = await get_data(client,token_pair=my_symbol+'USDT')
                    priceBUSD = await get_data(client,token_pair=my_symbol+'BUSD')
                    print('SELLING : ',my_symbol+'USDT ',priceUSDT,'\t|\t',my_symbol+'BUSD : ',priceBUSD)
                
                    if priceUSDT < priceBUSD:
                        sell_stablecoin='BUSD'

                    if priceUSDT > priceBUSD:
                        sell_stablecoin='USDT'
                    
                    sell_symbol = deepcopy(my_symbol+sell_stablecoin)
                    prezzo_minimo_vendita = max(priceUSDT,priceBUSD)
                    prezzo_di_apertura = orderbookBUY[i]['prezzo_di_apertura_buy']
                    
                                                                 # 20 =>        prezzo di SELL  >= 1.2 * prezzo di BUY
                    if prezzo_minimo_vendita >= (( (minimo_guadagno_percentuale_sell+commissioniSpotMaker)/100) + 1) * prezzo_di_apertura :

                        order = await client.order_limit_sell(timeInForce='GTC',
                                            symbol = sell_symbol,
                                            quantity = await format_coin_quantity(coin_quantity,symbol=sell_symbol),
                                            price = round(float(prezzo_minimo_vendita),2)) # round 2, or 4


                    print_OPEN(order)
                    print_FILLED(order)

                    orderbookSELL.append(order)
                    #FILLED_orders.append(orderbookBUY[i])
                    orderbookBUY.remove(orderbookBUY[i])

        if len(orderbookSELL)>0:
            for i in range(len(orderbookSELL)):
                if orderbookSELL[i]['status']=='FILLED':
                    #FILLED_orders.append(orderbookSELL[i])
                    print_FILLED(orderbookSELL[i])
                    orderbookSELL.remove(orderbookSELL[i])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())