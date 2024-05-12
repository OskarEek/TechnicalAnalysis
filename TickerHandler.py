import time
import threading
import os

class TickerHandler:
    def __init__(self, chartTimeSeconds):
        self.stop_flag = threading.Event()
        self.gains = []
        self.loss = []
        self.rsi = 0
        self.previous_price = 0
        self.print_data_keys = ['id', 'price']
        self.chart_time = chartTimeSeconds

        self.listen_price = False
        self.chart_timer_thread = threading.Thread(target=self.toggle_price_listen)
        self.chart_timer_thread.start()

    def print_data(self, data, printArrs):
        os.system('cls')
        print_string = "======================================================\n\n"
        for key in data:
            if key in self.print_data_keys or len(self.print_data_keys) == 0:
                print_string += (key + ": " + str(data[key]) + "\n")

        print_string += "\n"
        print_string += "RSI: " + str(self.rsi) + "\n"
        print_string += "\n" 

        if (printArrs and self.rsi == 0) or (len(self.gains) > 0 and self.rsi == 0):
            print_string += "Gains: " + str(self.gains) + "\n" 
            print_string += "Loss: " + str(self.loss) + "\n"
        
        print_string += "\n=====================================================\n"
        print(print_string)

    def on_message(self, ws, data):
        if self.stop_flag.is_set():
            ws.close()
        else:
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

            self.print_data(data, False)
            self.calulate_rsi(currentGain, currentLoss)

    def signal_handler(self, sig, frame):
        print("Ctrl+C detected. Stopping the threads.")
        self.stop_flag.set()
        self.terminate_threads()

    def calulate_rsi(self, currentGain, currentLoss):
        if len(self.gains) >= 13:
            # Get the last 13 recorded gains and losses
            lastGains = self.gains[-13:]
            lastLoss = self.loss[-13:]

            avgGains = (sum(lastGains) + currentGain) / 14
            avgLoss = (sum(lastLoss) + currentLoss) / 14

            if avgLoss == 0:
                self.rsi = 100  # Avoid division by zero, RSI is 100 if average loss is zero
            else:
                rs = avgGains / avgLoss
                self.rsi = 100 - (100 / (1 + rs))

            # Update the lists to only contain the last 14 entries
            self.gains = self.gains[-14:]
            self.loss = lastLoss[-14:]
    
    def toggle_price_listen(self):
        print("Toggling price listener")
        while not self.stop_flag.is_set():
            time.sleep(self.chart_time)
            self.listen_price = True

    def terminate_threads(self):
        self.chart_timer_thread.join()