# GreenRock
### Trading arbitrage bot in the Binance exchange 

# COSTI
swap 10 centesimi

### COPPIE USDT/BUSD 
- X/BUSD
- X/usdt
- BUSD/usdt

### COPPIE BNB/BUSD
- X/BUSD
- X/BNB
- BUSD/BNB

## ERRORI
APIError(code=-1013): Filter failure: MIN_NOTIONAL

## INSTALLAZIONE
Devi avere python3 per continuare 

1. Upgrade pip
```python 
python3 -m pip install --upgrade pip 
```

2. Install python-binance
```python 
python3 -m pip install --upgrade python-binance

```

3. export api secrets in the shell eviroement 
```python 
export binance_api="your api key"
export binance_secret="your api secret"
```

## LANCIA IL BOT
```python
python3 bot.py
```
