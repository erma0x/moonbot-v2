#!/usr/bin/env python3.7
# coding: utf-8
"""
try to get real time data seconds by seconds
"""
from binance import ThreadedWebsocketManager
import time 
symbol = 'BNBBTC'

twm = ThreadedWebsocketManager()
# start is required to initialise its internal loop
twm.start()

def handle_socket_message(msg):
    print(f"message type: {msg['e']}")
    print(msg)
    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

depth_stream_name = twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)


time.sleep(10)
twm.stop_socket(depth_stream_name)
