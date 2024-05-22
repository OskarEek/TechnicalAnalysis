import yliveticker
from TickerHandler import TickerHandler

hourly = 'H'
minute = 'M'
second = 'S'

ticker_names = ["QQQ"]


handler = TickerHandler(minute, ticker_names)
try:
    yliveticker.YLiveTicker(on_ticker=handler.on_message, ticker_names=ticker_names)
finally:
    handler.stop_flag.set()