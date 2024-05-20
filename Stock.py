import os
from Calculator import Calculator
from colorama import Fore
from colorama import init as colorama_init
from datetime import datetime, timezone

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.gains = []
        self.loss = []

        self.rsi = 0
        self.rsi30 = False
        self.rsi70 = False

        self.last_stored_price = 0
        self.current_data = None
        self.previous_data = None
        
        self.store_new_price = False
        self.print_data_keys = []
        colorama_init(autoreset=True)

        self.default_print_color = Fore.WHITE #TODO: move this constant to a config file of some sort?

    def update(self, data):
        self.previous_data = self.current_data
        self.current_data = data

        price = data['price']
        if self.last_stored_price == 0:
            self.last_stored_price = price
            return
            
        price_change = price - self.last_stored_price
        change_percent = price_change / self.last_stored_price

        currentGain = change_percent if change_percent > 0 else 0
        currentLoss = -change_percent if change_percent < 0 else 0
            
        if self.store_new_price:
            self.gains.append(currentGain)
            self.loss.append(currentLoss)

            self.last_stored_price = price
            self.print_data(True)
            self.store_new_price = False
            return


        currentRsi = Calculator.calulate_rsi(self.gains, self.loss, currentGain, currentLoss)
        if self.rsi >= 70 and currentRsi < 70:
            self.rsi70 = True
        elif self.rsi <= 30 and currentRsi > 30:
            self.rsi30 = True
        self.rsi = currentRsi

        self.print_data(False)
    
    def print_data(self, printArrs):
        if self.current_data == None:
            return

        os.system('cls') #TODO: if we're listening on multiple stocks we do not want to clear console every time, figure out another solution
        print_string = self.default_print_color + "======================================================\n\n"
        for key in self.current_data:
            if len(self.print_data_keys) == 0 or key in self.print_data_keys:
                color = self.default_print_color
                value = self.current_data[key]
                if key == 'price':
                    color = Fore.GREEN if self.current_data[key] >= self.previous_data[key] else Fore.RED
                if key == 'timestamp':
                    value = self.convert_timestamp(value)
    
                print_string += (key + ": " + color + str(value) + self.default_print_color + "\n")

        print_string += "\n"
        print_string += "RSI: " + str(self.rsi) + "\n"

        print_string += "\n"
        print_string += "RSI crossed 70: " + (Fore.GREEN if self.rsi70 else self.default_print_color) + str(self.rsi70) + self.default_print_color + "\n"

        print_string += "RSI crossed 30: " + (Fore.GREEN if self.rsi30 else self.default_print_color) + str(self.rsi30) + self.default_print_color + "\n"
        print_string += "\n" 

        if (printArrs and self.rsi == 0) or (len(self.gains) > 0 and self.rsi == 0):
            print_string += "Gains: " + str(self.gains) + "\n" 
            print_string += "Loss: " + str(self.loss) + "\n"
        
        print_string += "\n=====================================================\n"
        print(print_string)
    
    def convert_timestamp(self, timestamp_ms):
        timestamp_s = timestamp_ms / 1000
        date_time = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
        return date_time.strftime('%Y-%m-%d %H:%M:%S')

    def toggle_store_new_price(self):
        self.store_new_price = not self.store_new_price