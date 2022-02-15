#!/usr/bin/env python3.7
# coding: utf-8
"""
try to get real time data seconds by seconds
"""
import requests

LINK = "wss://stream.binance.com:9443/ws/btcusdt@trade"

x = requests.get(LINK)

print(x.text)