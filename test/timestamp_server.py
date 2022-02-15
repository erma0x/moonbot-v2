#!/usr/bin/env python3.7
# coding: utf-8
"""
try to convert token price in correct manner
"""
from datetime import datetime

def converti_timestamp_in_data(time="1644599819999"):
    time=str(time)
    return(datetime.fromtimestamp(int(time[:-3])).strftime('%d-%m-%Y %H:%M:%S'))
