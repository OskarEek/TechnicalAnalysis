import time
import threading
import os
from DataDto import DataDto
from Stock import Stock 
from Datapoint import Datapoint
import yfinance as yf
from datetime import datetime

class TickerHandler:
    def __init__(self, chart, tickerNames):
        self.stocks = [Stock(x, chart, self.get_history(x)) for x in tickerNames]
        self.stop_flag = threading.Event()


    def on_message(self, ws, data):
        if self.stop_flag.is_set():
            ws.close()
        else:
            dataDto = DataDto(data)
            stock = self.get_stock_from_id(dataDto.id)
            stock.update(dataDto)

            os.system('cls')
            for stock in self.stocks:
                stock.print_data()
                

    def get_stock_from_id(self, id):
        stockResult = [x for x in self.stocks if x.ticker == id]
        assert(len(stockResult) == 1)
        return stockResult[0]

    def get_history(self, ticker) -> list[Datapoint]:
        msft = yf.Ticker(ticker)
        hist = msft.history(period="1mo", interval="1h")

        result = []
        for index, row in hist.iterrows():
            datapoint = Datapoint(row['Close'], self.get_timestamp(str(index)), minPrice=row['Low'], maxPrice=row['High'])
            if len(result) > 0:
                datapoint.calc_loss_gains(result[-1])
            result.append(datapoint)

        return result

    def get_timestamp(self, date_str):
        date_obj = datetime.fromisoformat(date_str)
        # Getting the timestamp in milliseconds
        return int(date_obj.timestamp() * 1000)



