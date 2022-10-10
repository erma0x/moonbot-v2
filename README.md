# Moonbot trading robot 🤖 
### Triangular arbitrage in binance.com 

![](docs/moonbot.jpeg)

### Triangular arbitrage

Triangular arbitrage is different from Spatial and proceeds on a single exchange. It does not rely on the asset’s price differences between trading platforms. Rather focuses on exploiting the price differences between trading pairs.
As the name conveys, triangular arbitrage involves three different assets, in our case, cryptocurrencies listed on the same exchange. The strategy is based on trading asset A for asset B, asset B for asset C, and finally asset C back to asset A to earn a profit.
Opportunities for triangular crypto arbitrage arise from price differences between three (or more) cryptocurrencies. Traders are looking for cases when a specific coin is undervalued compared to the other and overvalued compared to the third. They profit from the conversion differences.



## Workflow
1. Get real time data from Binance on the prices of the pairs you are looking for.

2. Set the minimum price difference between two pairs (e.g. X / BUSD and X / USDT) in order to open a BUY LIMIT operation on a spot

3. after the transaction has been filled, he sells spots to market in the other pair

![](docs/TriangularArbitrage.png)

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

### Trading pairs with USDT/BUSD 
- X/BUSD
- X/USDT
- BUSD/USDT

### Trading pairs with BNB/BUSD
- X/BUSD
- X/BNB
- BUSD/BNB


