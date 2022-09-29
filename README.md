# Moonbot trading robot 🤖 
### Market-neutral arbitrage in binance.com 

![](docs/moonbot.jpeg)


## Workflow
1. Get real time data from Binance on the prices of the pairs you are looking for.

2. Set the minimum price difference between two pairs (e.g. X / BUSD and X / USDT) in order to open a BUY LIMIT operation on a spot

3. after the transaction has been filled, he sells spots to market in the other pair

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

<br>

## Trading costs
swap : 10 cents $

### Pairs with USDT/BUSD 
- X/BUSD
- X/usdt
- BUSD/usdt

###  Pairs with BNB/BUSD
- X/BUSD
- X/BNB
- BUSD/BNB


