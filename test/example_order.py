"""
    order object example
    {'symbol': 'ETHBUSD', 'orderId': 7760933105, 'orderListId': -1, 
    'clientOrderId': 'RKPcQ9jAOT8LlUYK3xygGB', 'transactTime': 1644342622758, 
    'price': '3040.28000000', 'origQty': '0.00490000', 'executedQty': '0.00000000', 
    'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC',
    'type': 'LIMIT', 'side': 'BUY', 'fills': []}

  {'symbol': 'ETHUSDT', 'orderId': 7848161625, 'orderListId': -1, 
  'clientOrderId': 'v72bYrotvtxkic5V1LgnvH', 'transactTime': 1644865734686, 
  'price': '3040.00000000', 'origQty': '0.00520000', 'executedQty': '0.00520000', 
  'cummulativeQuoteQty': '14.99368000', 'status': 'FILLED',
   'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'SELL', 
  'fills': [{'price': '2883.40000000', 'qty': '0.00520000', 
  'commission': '0.00002826', 'commissionAsset': 'BNB', 'tradeId': 757775818}]}

order = await client.order_limit_buy(timeInForce='GTC',
                    symbol = symbol+stablecoin,
                    quantity = await format_coin_quantity(coin_quantity),
                    price = round(float(lower_price_stablecoin),4)) # round 2, or 4



order = await client.create_order(
    symbol=symbol+stablecoin,
    side=client.SIDE_BUY,
    type=client.ORDER_TYPE_MARKET,
    timeInForce='60',
    quantity= await format_coin_quantity(coin_quantity, symbol = symbol+stablecoin))


"""