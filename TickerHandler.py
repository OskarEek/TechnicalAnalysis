import time
import threading
import os
from Stock import Stock 

class TickerHandler:
    def __init__(self, chartTimeSeconds, tickerNames):
        self.stocks = [Stock(x) for x in tickerNames]
        self.chart_time = chartTimeSeconds

        self.stop_flag = threading.Event()
        self.chart_timer_thread = threading.Thread(target=self.toggle_price_listen)
        self.chart_timer_thread.start()


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
    

    def signal_handler(self, sig, frame):
        print("Ctrl+C detected. Stopping the threads.")
        self.stop_flag.set()
        self.terminate_threads()

    def toggle_price_listen(self):
        print("Toggling price listener")
        while not self.stop_flag.is_set():
            for stock in self.stocks:
                stock.toggle_store_new_price()
            time.sleep(self.chart_time)

    def terminate_threads(self):
        self.chart_timer_thread.join()