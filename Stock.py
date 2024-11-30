import pytz
import math
from typing import Optional
from Calculator import Calculator
from colorama import Fore
from colorama import init as colorama_init
from datetime import datetime, timezone
from Datapoint import Datapoint
from DataDto import DataDto
from Level import Level
from Constants.timeconstants import hour, half_hour

class Stock:
    def __init__(self, ticker, chart, datapoints: list[Datapoint] = []):
        #Constants
        self.ticker = ticker
        self.chart = chart

        #Indicators
        self.rsi30 = False
        self.rsi70 = False
        self.bullish_divergence = False
        self.bearish_divergence = False
        self.supports: list[Level]= []
        self.resistances: list[Level] = []

        #Stock data
        self.datapoints: list[Datapoint] = datapoints
        self.current_data: Datapoint = None
        self.previous_data: Datapoint = None

        #Updates resets every time a new datapoint is stored
        self.last_chart_update_time = None
        self.lowest_price = None
        self.highest_price = None
        
        #Print
        colorama_init(autoreset=True)
        self.default_print_color = Fore.WHITE #TODO: move this constant to a config file of some sort?



    def update(self, data: DataDto):
        self.previous_data = self.current_data
        self.current_data = Datapoint(data.price, data.timestamp)

        if self.previous_data == None:
            return
 
        self.current_data.calc_loss_gains(self.previous_data)
        self.current_data.rsi = Calculator.calulate_rsi(self.datapoints, self.current_data.gain, self.current_data.loss)

        if len(self.datapoints) == 0:
            dp: Optional[Datapoint] = self.new_datapoint_to_store(self.previous_data, self.current_data)
            if dp == None:
                return
            dp.max_price = dp.price
            dp.min_price = dp.price
            dp.timestamp = self.round_to_closest_half_hour(dp.timestamp)
            
        self.toggle_rsi_indicators() 
        self.find_levels()
            
        newDpToStore: Optional[Datapoint] = self.new_datapoint_to_store(self.previous_data, self.current_data)
        if newDpToStore != None:
            newDpToStore.max_price = self.highest_price if not self.highest_price == None else newDpToStore.price
            newDpToStore.min_price = self.lowest_price if not self.lowest_price == None else newDpToStore.price
            self.lowest_price = None
            self.highest_price = None

            lastStoredDp = self.datapoints[-1]
            newDpToStore.calc_loss_gains(lastStoredDp)
            newDpToStore.timestamp = lastStoredDp.timestamp + hour

            self.datapoints.append(newDpToStore)
        
        if self.lowest_price == None or self.current_data.price < self.lowest_price:
            self.lowest_price = self.current_data.price
        if self.highest_price == None or self.current_data.price > self.highest_price:
            self.highest_price = self.current_data.price





    def print_data(self):
        if self.current_data == None:
            return

        print_string = self.default_print_color + "==================================================\n\n"
        print_string += "Stock: " + self.ticker + "\n"

        if not self.previous_data == None:
            print_string += "Price: " + self.get_colored_string((Fore.GREEN if self.current_data.price >= self.previous_data.price else Fore.RED), str(self.current_data.price)) + "\n"
            print_string += "Change percent: " + self.get_colored_string((Fore.GREEN if self.current_data.price >= self.previous_data.price else Fore.RED), str(self.current_data.change_percentage)) + "\n"
        else:
            print_string += "Price: " + str(self.current_data.price) + "\n"
            print_string += "Change percent: " + str(self.current_data.change_percentage) + "\n"

        print_string += "Timestamp: " + self.current_data.timestamp_est() + "\n"

        print_string += "\n"
        print_string += "RSI: " + str(self.current_data.rsi) + "\n\n"

        print_string += "RSI crossed 70: " + self.get_colored_string((Fore.GREEN if self.rsi70 else self.default_print_color), str(self.rsi70)) + "\n"
        print_string += "RSI crossed 30: " + self.get_colored_string((Fore.GREEN if self.rsi30 else self.default_print_color), str(self.rsi30)) + "\n\n"

        print_string += "Bearish divergence: " + self.get_colored_string((Fore.GREEN if self.bearish_divergence else self.default_print_color), str(self.bearish_divergence)) + "\n"
        print_string += "Bullish divergence: " + self.get_colored_string((Fore.GREEN if self.bullish_divergence else self.default_print_color), str(self.bullish_divergence)) + "\n\n"

        print_string += "Supports: \n"
        for x in self.supports:
            print_string += "   Price: " + str(x.value) + " | Strength: " + str(x.strength) + "\n"
        print_string += "\nResistances: \n"
        for x in self.resistances:
            print_string += "   Price: " + str(x.value) + " | Strength: " + str(x.strength) + "\n"

        #if (printArrs and self.current_data.rsi == 0) or (len(self.datapoints) > 0 and self.current_data.change_percentage == 0):
        #    print_string += "Gains: " + str([x.gain for x in self.datapoints]) + "\n" 
        #    print_string += "Loss: " + str([x.loss for x in self.datapoints]) + "\n"
        
        print_string += "\n==================================================\n"

        print_string += "\n"
        print_string += "Number of datapoints: " + str(len(self.datapoints))
        print_string += "\n"
        lastDp = self.datapoints[-13:]
        for dp in lastDp:
            print_string += "Datapoint: " + dp.timestamp_est()
            print_string += " | Price: " + str(dp.price) + " | Gains: " + str(dp.gain) + " | Loss: " + str(dp.loss)
            print_string += "\n"
            
        print(print_string)
        prices = [x.price for x in lastDp]
        print(prices)


    def get_colored_string(self, color, value):
        return color + str(value) + self.default_print_color


    def get_chart_time(self, chart, timestamp_ms):
        timestamp_s = timestamp_ms / 1000
        utc_dt = datetime.fromtimestamp(timestamp_s, tz=pytz.utc)
        est = pytz.timezone('America/New_York')
        est_dt = utc_dt.astimezone(est)
        return est_dt.strftime('%' + 'M')



    def new_datapoint_to_store(self, previousDp: Datapoint, newDp: Datapoint) -> Datapoint:
        if previousDp.timestamp % hour < half_hour and newDp.timestamp % hour > half_hour:
            return previousDp
        elif newDp.timestamp % hour == half_hour:
            return newDp

        return None
    
    def round_to_closest_half_hour(timestamp_ms: int) -> int:
        # Convert milliseconds to seconds and get the time in hours and minutes
        seconds = timestamp_ms / 1000
        minutes = (seconds // 60) % 60
        hours = (seconds // 3600) % 24

        # Calculate total minutes and round to the nearest half hour (30 minutes)
        total_minutes = hours * 60 + minutes
        rounded_minutes = math.ceil(total_minutes / 30) * 30

        # Convert the rounded time back to milliseconds
        rounded_hours = rounded_minutes // 60
        rounded_minute = rounded_minutes % 60

        # Calculate new timestamp
        rounded_timestamp_ms = (rounded_hours * 3600 + rounded_minute * 60) * 1000

        return rounded_timestamp_ms
    
    def toggle_rsi_indicators(self):
        if self.previous_data.rsi >= 70 and self.current_data.rsi < 70:
            self.rsi70 = True
        elif self.previous_data.rsi <= 30 and self.current_data.rsi > 30:
                self.rsi30 = True

        if self.rsi30 and (self.current_data.rsi >= 50 or self.current_data.rsi < 29.5):
            self.rsi30 = False
        if self.rsi70 and (self.current_data.rsi <= 50 or self.current_data.rsi > 70.5):
            self.rsi70 = False

    def find_levels(self):
        self.supports = Calculator.find_support(self.datapoints)
        self.resistances = Calculator.find_resistance(self.datapoints)
