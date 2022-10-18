# Moonbot trading robot 🤖 
### Trading pair arbitrage in binance.com 

![](docs/moonbot.jpeg)


## Trading strategy example

Check for X/BUSD and X/USDT change
   - if X/BUSD / X/USDT > 1.001
       - BUY X/USDT and SELL X/BUSD
   - X/BUSD / X/USDT < 0.999
      - SELL X/USDT and BUY X/BUSD

#### Trading pairs with USDT/BUSD 
- X/BUSD
- X/USDT
- BUSD/USDT

#### Trading pairs with BNB/BUSD
- X/BUSD
- X/BNB
- BUSD/BNB

## How to run 
1. ```source venv/bin/activate```
2. ```export binance_api="your api key"```
3. ```export binance_secret="your api secret"```
4. ```python3 bot.py```


## How to install
1. ```python3 -m venv venv```
2. ```source venv/bin/activate```
3. ```python3 -m pip install --upgrade pip```
4. ```python3 -m pip install --upgrade python-binance```
5. ```export binance_api="your api key"```
5. ```export binance_secret="your api secret"```
