#!/usr/bin/env python3.7
# coding: utf-8
"""
try to get real time data seconds by seconds
"""

#wscat -c wss://stream.binance.com:9443/ws/btcusdt@trade
import ssl
import websocket
import requests
import asyncio, ssl, websockets

LINK = "wss://stream.binance.com:9443/ws/btcusdt@trade"


# ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
# print(ws.connect(LINK))

#todo kluge
#HIGHLY INSECURE
ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
#HIGHLY INSECURE
#todo kluge

LINK = "wss://myAwesomeSSL.wss.kluge"

async with websockets.connect(LINK, ssl=ssl_context) as websocket:
        greeting = await websocket.recv()
        print(f"< {greeting}")
