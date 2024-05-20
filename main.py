import yliveticker
import time
import threading
import signal
from TickerHandler import TickerHandler


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