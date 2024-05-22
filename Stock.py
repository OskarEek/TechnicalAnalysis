import os
from Calculator import Calculator
from colorama import Fore
from colorama import init as colorama_init
from datetime import datetime, timezone
from Datapoint import Datapoint

class Stock:
    def __init__(self, ticker, chart):
        #Constants
        self.ticker = ticker
        self.chart = chart

        #Indicators
        self.rsi30 = False
        self.rsi70 = False
        self.bullish_divergence = False
        self.bearish_divergence = False

        #Stock data
        self.datapoints: list[Datapoint] = []
        self.current_data: Datapoint = None
        self.previous_data: Datapoint = None
        self.last_chart_update_time = None
        
        #Print
        colorama_init(autoreset=True)
        self.default_print_color = Fore.WHITE #TODO: move this constant to a config file of some sort?



    def update(self, data):
        self.previous_data = self.current_data
        self.current_data = Datapoint(data['price'], self.convert_timestamp(data['timestamp']))
        chartTime = self.get_chart_time(data['timestamp'])

        if self.last_chart_update_time == None:
            if not self.last_chart_update_time == chartTime:
                self.last_chart_update_time = chartTime
            return
            
        price_change = self.current_data.price - self.previous_data.price
        self.current_data.change_percentage = price_change / self.previous_data.price
        self.current_data.gain = self.current_data.change_percentage if self.current_data.change_percentage > 0 else 0
        self.current_data.loss = -self.current_data.change_percentage if self.current_data.change_percentage < 0 else 0

        self.current_data.rsi = Calculator.calulate_rsi(self.datapoints, self.current_data.gain, self.current_data.loss)
        if not self.previous_data == None:
            if self.previous_data.rsi >= 70 and self.current_data.rsi < 70:
                self.rsi70 = True
            elif self.previous_data.rsi <= 30 and self.current_data.rsi > 30:
                self.rsi30 = True
            
        if not self.last_chart_update_time == chartTime:
            self.datapoints.append(self.previous_data)
            self.last_chart_update_time = chartTime 



    def print_data(self, printArrs=False):
        if self.current_data == None:
            return

        print_string = self.default_print_color + "======================================================\n\n"
        print_string += "Stock: " + self.ticker + "\n"

        if not self.previous_data == None:
            print_string += "Price: " + self.get_colored_string((Fore.GREEN if self.current_data.price >= self.previous_data.price else Fore.RED), str(self.current_data.price)) + "\n"
            print_string += "Change percent: " + self.get_colored_string((Fore.GREEN if self.current_data.price >= self.previous_data.price else Fore.RED), str(self.current_data.change_percentage)) + "\n"
        else:
            print_string += "Price: " + str(self.current_data.price) + "\n"
            print_string += "Change percent: " + str(self.current_data.change_percentage) + "\n"

        print_string += "Timestamp: " + self.current_data.timestamp + "\n"

        print_string += "\n"
        print_string += "RSI: " + str(self.current_data.rsi) + "\n\n"

        print_string += "RSI crossed 70: " + self.get_colored_string((Fore.GREEN if self.rsi70 else self.default_print_color), str(self.rsi70)) + "\n"
        print_string += "RSI crossed 30: " + self.get_colored_string((Fore.GREEN if self.rsi30 else self.default_print_color), str(self.rsi30)) + "\n\n"

        print_string += "Bearish divergence: " + self.get_colored_string((Fore.GREEN if self.bearish_divergence else self.default_print_color), str(self.bearish_divergence)) + "\n"
        print_string += "Bullish divergence: " + self.get_colored_string((Fore.GREEN if self.bullish_divergence else self.default_print_color), str(self.bullish_divergence)) + "\n\n"

        #if (printArrs and self.current_data.rsi == 0) or (len(self.datapoints) > 0 and self.current_data.change_percentage == 0):
        #    print_string += "Gains: " + str([x.gain for x in self.datapoints]) + "\n" 
        #    print_string += "Loss: " + str([x.loss for x in self.datapoints]) + "\n"
        
        print_string += "\n=====================================================\n"
        print(print_string)

    def get_colored_string(self, color, value):
        return color + str(value) + self.default_print_color

    
    def convert_timestamp(self, timestamp_ms):
        timestamp_s = timestamp_ms / 1000
        date_time = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
        return date_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_chart_time(self, timestamp_ms):
        timestamp_s = timestamp_ms / 1000
        date_time = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
        return date_time.strftime('%' + self.chart)


