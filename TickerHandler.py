import time
import threading
import os
from Stock import Stock 

class TickerHandler:
    def __init__(self, chart, tickerNames):
        self.stocks = [Stock(x, chart) for x in tickerNames]
        self.stop_flag = threading.Event()


    def on_message(self, ws, data):
        if self.stop_flag.is_set():
            ws.close()
        else:
            stock = self.get_stock_from_id(data['id'])
            stock.update(data)

            os.system('cls')
            for stock in self.stocks:
                stock.print_data()
                

    def get_stock_from_id(self, id):
        stockResult = [x for x in self.stocks if x.ticker == id]
        assert(len(stockResult) == 1)
        return stockResult[0]