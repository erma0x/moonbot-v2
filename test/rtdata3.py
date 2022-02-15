#!/usr/bin/env python3.7
# coding: utf-8
"""
try to get real time data seconds by seconds
"""

#wscat -c wss://stream.binance.com:9443/ws/btcusdt@trade # <-- BASH COMMAND FOR REAL TIME DATA
import ssl
import websocket
import requests
LINK = "wss://stream.binance.com:9443/ws/btcusdt@trade"
ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
print(ws.connect(LINK))
