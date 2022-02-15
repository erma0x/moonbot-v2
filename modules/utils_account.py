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

async def get_stream_data(binanceSocketManager,token):
    while True:
        res = await binanceSocketManager.kline_socket(symbol=token+'USDT').recv()
        print('symbol: ',res['s'],' date: ',timestamp_to_datetime(res['k']['T']), ' closing price: ',res['k']['c'] , ' volume: ',res['k']['V'])
