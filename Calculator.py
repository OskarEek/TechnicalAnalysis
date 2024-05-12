import numpy as np
from scipy.signal import argrelextrema

class Calculator:

    def calulate_rsi(self, gains, loss, currentGain, currentLoss):
        if len(gains) >= 13:
            # Get the last 13 recorded gains and losses
            lastGains = gains[-13:]
            lastLoss = loss[-13:]

            avgGains = (sum(lastGains) + currentGain) / 14
            avgLoss = (sum(lastLoss) + currentLoss) / 14

            if avgLoss == 0:
                #self.rsi = 100  # Avoid division by zero, RSI is 100 if average loss is zero
                return 100
            else:
                rs = avgGains / avgLoss
                return 100 - (100 / (1 + rs))

            # Update the lists to only contain the last 14 entries
            #self.gains = self.gains[-14:]
            #self.loss = lastLoss[-14:]

        return 0

    def is_negative_divergance():
        pass

    def is_positive_divergence():
        pass

    def find_list_peaks(values, order=5):
        npArray = np.array(values)
        # Find indices of all local maxima
        peak_indices = argrelextrema(npArray, np.greater, order=order)[0]
        return peak_indices 

    def find_list_lows(values, order=5):
        npArray = np.array(values)
        # Find indices of all local minima
        minima_indices = argrelextrema(npArray, np.less, order=order)[0]
        return minima_indices 