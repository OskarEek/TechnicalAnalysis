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

        return 0

    def is_bearish_divergence(datapoints, nrOfPeaks):
        #There is bearish divergence if rsi make lower highs and stock prive makes higher highs

        numberOfDataPoints = 31 * 7 #31 days, 7 datapoints on the hourly chart each day
        selectedDatapoints = datapoints[-numberOfDataPoints:]

        rsiDataPoints = [x.RSI for x in selectedDatapoints]
        rsiPI = Calculator.find_list_peaks(rsiDataPoints, 10) #May need to tweek the order (10) 
        if len(rsiPI) < nrOfPeaks:
            return False
        rsiPI.sort()
        rsiPI = rsiPI[-nrOfPeaks:]

        for i in range(len(rsiPI) - 1):
            rsiIndex = rsiPI[i]
            rsiIndex2 = rsiPI[i + 1]
            if rsiDataPoints[rsiIndex] <= rsiDataPoints[rsiIndex2]:  #Should I have just "<" or "<=" here? 
                return False


        priceDataPoints = [x.Price for x in selectedDatapoints]
        pricePI = Calculator.find_list_peaks(priceDataPoints, 10) #May need to tweek the order (10)
        if len(pricePI) < nrOfPeaks:
            return False
        pricePI.sort()
        pricePI = pricePI[-nrOfPeaks:]

        for i in range(len(pricePI) - 1):
            priceIndex = pricePI[i]
            priceIndex2 = pricePI[i + 1]
            if priceDataPoints[priceIndex] >= priceDataPoints[priceIndex2]:
                return False
                
        return True



    def is_bullish_divergence(datapoints, nrOfPeaks):
        #There is bullish divergence if stock price makes lower lows and RSI makes higher lows

        numberOfDataPoints = 31 * 7 #31 days, 7 datapoints on the hourly chart each day
        selectedDatapoints = datapoints[-numberOfDataPoints:]

        rsiDataPoints = [x.RSI for x in selectedDatapoints]
        rsiLI= Calculator.find_list_lows(rsiDataPoints, 10) #May need to tweek the order (10) 
        if len(rsiLI) < nrOfPeaks:
            return False
        rsiLI.sort()
        rsiLI = rsiLI[-nrOfPeaks:]

        for i in range(0, len(rsiLI) - 1):
            rsiIndex = rsiLI[i]
            rsiIndex2 = rsiLI[i + 1]
            if rsiDataPoints[rsiIndex] >= rsiDataPoints[rsiIndex2]:  #Should I have just "<" or "<=" here? 
                return False


        priceDataPoints = [x.Price for x in selectedDatapoints]
        priceLI = Calculator.find_list_lows(priceDataPoints, 10) #May need to tweek the order (10)
        if len(priceLI) < nrOfPeaks:
            return False
        priceLI.sort()
        priceLI = priceLI[-nrOfPeaks:]

        for i in range(0, len(priceLI) - 1):
            priceIndex = priceLI[i]
            priceIndex2 = priceLI[i + 1]
            if priceDataPoints[priceIndex] <= priceDataPoints[priceIndex2]:
                return False
                
        return True

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