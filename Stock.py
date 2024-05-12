import os
from Calculator import Calculator

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.gains = []
        self.loss = []
        self.rsi = 0
        self.previous_price = 0
        self.last_update_data = None
        
        self.store_new_price = False
        self.print_data_keys = ['id', 'price']

    def update(self, data):
        self.last_update_data = data

        price = data['price']
        if self.previous_price == 0:
            self.previous_price = price
            return
            
        price_change = price - self.previous_price
        change_percent = price_change / self.previous_price

        currentGain = change_percent if change_percent > 0 else 0
        currentLoss = -change_percent if change_percent < 0 else 0
            
        if self.listen_price:
            self.gains.append(currentGain)
            self.loss.append(currentLoss)

            self.previous_price = price
            self.print_data(data, True)
            self.listen_price = False
            return

        self.rsi = Calculator.calulate_rsi(self.gains, self.loss, currentGain, currentLoss)
        self.print_data(data, False)
    
    def print_data(self, printArrs):
        if self.last_update_data == None:
            return

        os.system('cls')
        print_string = "======================================================\n\n"
        for key in self.last_update_data:
            if key in self.print_data_keys or len(self.print_data_keys) == 0:
                print_string += (key + ": " + str(self.last_update_data[key]) + "\n")

        print_string += "\n"
        print_string += "RSI: " + str(self.rsi) + "\n"
        print_string += "\n" 

        if (printArrs and self.rsi == 0) or (len(self.gains) > 0 and self.rsi == 0):
            print_string += "Gains: " + str(self.gains) + "\n" 
            print_string += "Loss: " + str(self.loss) + "\n"
        
        print_string += "\n=====================================================\n"
        print(print_string)
    
    def toggle_store_new_price(self):
        self.store_new_price = not self.store_new_price