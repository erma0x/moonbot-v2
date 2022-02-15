
async def get_balance(client):
    USDT_balance = await client.get_asset_balance(asset='USDT')
    BUSD_balance = await client.get_asset_balance(asset='BUSD')
    print('YOUR BALANCE in: \n- USDT balance : ',USDT_balance['free'],'\n- BUSD balance : ',BUSD_balance['free'])
    return USDT_balance, BUSD_balance