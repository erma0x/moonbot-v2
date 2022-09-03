# Moonboot : let's arbitrage on Binance 🤖 


## Descrizione
Robot di arbitraggio all'interno di Binance.com

Prende i dati real time da Binance dei prezzi delle coppie che cerchi

Setta la differenza minima di prezzo fra due coppie (e.g. X/BUSD e X/USDT)
al fine di aprire un operazione BUY LIMIT su spot 
e dopo che e' stata fillata vendere a mercato  

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


