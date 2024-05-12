import yliveticker
import time
import threading
import signal
from TickerHandler import TickerHandler

minute = 60

handler = TickerHandler(minute)
signal.signal(signal.SIGINT, handler.signal_handler)


try:
    yliveticker.YLiveTicker(on_ticker=handler.on_message, ticker_names=["QQQ"])
finally:
    handler.stop_flag.set()
    handler.terminate_threads()