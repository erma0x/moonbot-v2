import asyncio
from re import T
from binance import AsyncClient, BinanceSocketManager
from timestamp_server import converti_timestamp_in_data

async def kline_listener(client):
    bm = BinanceSocketManager(client)
    async with bm.kline_socket(symbol='BNBBTC') as stream:
        while True:
            res = await stream.recv()
            print('date: ',converti_timestamp_in_data(res['k']['T']), '  price: ',res['k']['c'] , ' volume: ',res['k']['V'])

async def main():
    client = await AsyncClient.create()
    await kline_listener(client)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())