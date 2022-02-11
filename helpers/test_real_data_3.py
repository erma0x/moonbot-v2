
#wscat -c wss://stream.binance.com:9443/ws/btcusdt@trade
import ssl
import websocket
import requests
LINK = "wss://stream.binance.com:9443/ws/btcusdt@trade"
ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
print(ws.connect(LINK))
