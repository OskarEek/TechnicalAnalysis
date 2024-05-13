import numpy as np
from scipy.signal import argrelextrema

class Calculator:

    def calulate_rsi(gains, loss, currentGain, currentLoss):
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

    def is_bearish_divergence(datapoints, nrOfPeaks):
        #There is bearish divergence if rsi make lower highs and stock prive makes higher highs

        numberOfDataPoints = 31 * 7 #31 days, 7 datapoints on the hourly chart each day
        selectedDatapoints = datapoints[-numberOfDataPoints:]
        rsiDataPoints = [x.RSI for x in selectedDatapoints]

        rsiPI = Calculator.find_list_peaks(rsiDataPoints, 10) 
        if len(rsiPI) < nrOfPeaks:
            return False
        rsiPI = rsiPI.sort()
        rsiPI = rsiPI[-nrOfPeaks:]

        rsiLowerHighs = True
        for i in range(0, len(rsiPI) - 1):
            rsiIndex = rsiPI[i]
            if rsiDataPoints[rsiIndex] < rsiDataPoints[rsiIndex + 1]:  #Should I have just "<" or "<=" here? 
                rsiLowerHighs = False
                break

        if not rsiLowerHighs:
            return False
        
        #TODO: Check for higher highs in stock price
        priceDataPoints = [x.Price for x in selectedDatapoints]
        pass



    def is_bullish_divergence():
        pass

    def find_resistance():
        pass

    def find_support():
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