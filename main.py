import yliveticker
import time
import threading
import signal
from TickerHandler import TickerHandler

#== TODO =================================================================================================================
# 1. Implement following python package to get price history (seems like you can get hourly charts aswell)
#      - https://github.com/ranaroussi/yfinance
#      - https://github.com/ranaroussi/yfinance/wiki/Ticker#returns
#
# 2. Implement all calulation functions
#
# 3. Implement some way to only store new price point when a new hour begins (on a specific "klockslag") since we curre
#    don't get correct RSI calculations compared to tradingview since we get different datapoints compared to tradingview
#    since we dont store data points at the same moments as tradingview
#=========================================================================================================================


minute = 60
ticker_names = ["QQQ"]

handler = TickerHandler(minute, ticker_names)
signal.signal(signal.SIGINT, handler.signal_handler)

#TODO Implement try open new connection if websocket connection closes
try:
    yliveticker.YLiveTicker(on_ticker=handler.on_message, ticker_names=ticker_names)
finally:
    handler.stop_flag.set()
    handler.terminate_threads()