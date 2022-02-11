import requests

LINK = "wss://stream.binance.com:9443/ws/btcusdt@trade"

x = requests.get(LINK)

print(x.text)