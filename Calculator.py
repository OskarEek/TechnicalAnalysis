import numpy as np
from scipy.signal import argrelextrema
from Datapoint import Datapoint
from Level import Level

class Calculator:

    def calulate_rsi(datapoints: list[Datapoint], currentGain, currentLoss):
        period = 14  # Standard RSI period

        if len(datapoints) >= period:
            # Get the last 14 recorded gains and losses
            last_datapoints = datapoints[-period:]
            last_gains = [x.gain for x in last_datapoints]
            last_losses = [x.loss for x in last_datapoints]

            # Calculate the initial average gains and losses
            avg_gains = sum(last_gains) / period
            avg_losses = sum(last_losses) / period

            for i in range(period, len(datapoints)):
                current_gain = datapoints[i].gain
                current_loss = datapoints[i].loss

                # Exponentially smoothed averages
                avg_gains = ((avg_gains * (period - 1)) + current_gain) / period
                avg_losses = ((avg_losses * (period - 1)) + current_loss) / period

            avg_gains = ((avg_gains * (period - 1)) + currentGain) / period
            avg_losses = ((avg_losses * (period - 1)) + currentLoss) / period

            if avg_losses == 0:
                return 100  # RSI is 100 if average loss is zero
            else:
                rs = avg_gains / avg_losses
                return 100 - (100 / (1 + rs))

        return 0  # Not enough data to calculate RSI
        #if len(datapoints) >= 13:
        #    # Get the last 13 recorded gains and losses
        #    lastDatapoints = datapoints[-13:]
        #    lastGains = [x.gain for x in lastDatapoints]
        #    lastLoss = [x.loss for x in lastDatapoints]

        #    avgGains = (sum(lastGains) + currentGain) / 14
        #    avgLoss = (sum(lastLoss) + currentLoss) / 14

        #    if avgLoss == 0:
        #        #self.rsi = 100  # Avoid division by zero, RSI is 100 if average loss is zero
        #        return 100
        #    else:
        #        rs = avgGains / avgLoss
        #        return 100 - (100 / (1 + rs))

        #return 0

    def is_bearish_divergence(datapoints, nrOfPeaks):
        #There is bearish divergence if rsi make lower highs and stock prive makes higher highs
        numberOfDataPoints = 31 * 7 #31 days, 7 datapoints on the hourly chart each day
        selectedDatapoints = datapoints[-numberOfDataPoints:]

        rsiDataPoints = [x.RSI for x in selectedDatapoints]
        rsiPI = Calculator.find_list_peakIndexes(rsiDataPoints, 10) #May need to tweek the order (10) 
        if len(rsiPI) < nrOfPeaks:
            return False
        
        if Calculator.peaks_sorted_high_to_low(rsiDataPoints, rsiPI, nrOfPeaks):
            return False

        priceDataPoints = [x.Price for x in selectedDatapoints]
        pricePI = Calculator.find_list_peakIndexes(priceDataPoints, 10) #May need to tweek the order (10)
        if len(pricePI) < nrOfPeaks:
            return False

        if not Calculator.peaks_sorted_low_to_high():
            return False
                
        return True

    def is_bullish_divergence(datapoints, nrOfPeaks):
        #There is bullish divergence if stock price makes lower lows and RSI makes higher lows
        numberOfDataPoints = 31 * 7 #31 days, 7 datapoints on the hourly chart each day
        selectedDatapoints = datapoints[-numberOfDataPoints:]

        rsiDataPoints = [x.RSI for x in selectedDatapoints]
        rsiLI= Calculator.find_list_troughIndexes(rsiDataPoints, 10) #May need to tweek the order (10) 
        if len(rsiLI) < nrOfPeaks:
            return False

        if not Calculator.peaks_sorted_low_to_high(rsiDataPoints, rsiLI, nrOfPeaks):
            return False

        priceDataPoints = [x.Price for x in selectedDatapoints]
        priceLI = Calculator.find_list_troughIndexes(priceDataPoints, 10) #May need to tweek the order (10)
        if len(priceLI) < nrOfPeaks:
            return False

        if not Calculator.peaks_sorted_high_to_low(priceDataPoints, priceLI, nrOfPeaks):
            return False
                
        return True


    def find_resistance(datapoints: list[Datapoint]) -> list[Level]:
        values = [x.max_price for x in datapoints]
        peakIndexes = Calculator.find_list_peakIndexes(values, order=3)
        return Calculator.find_levels(values, peakIndexes)


    def find_support(datapoints: list[Datapoint]) -> list[Level]:
        values = [x.min_price for x in datapoints]
        peakIndexes = Calculator.find_list_troughIndexes(values, order=3)
        return Calculator.find_levels(values, peakIndexes)


    def find_list_peakIndexes(values, order=5):
        npArray = np.array(values)
        # Find indices of all local maxima
        peak_indices = argrelextrema(npArray, np.greater, order=order)[0]
        return peak_indices 

    def find_list_troughIndexes(values, order=5):
        npArray = np.array(values)
        # Find indices of all local minima
        minima_indices = argrelextrema(npArray, np.less, order=order)[0]
        return minima_indices 

    def peaks_sorted_high_to_low(values:list, peaks:list, nrOfPeaks=0):
        if nrOfPeaks == 0:
            nrOfPeaks = len(peaks)
        peaks.sort()
        peaks = peaks[-nrOfPeaks:]
        for i in range(len(values) - 1):
            rsiIndex = peaks[i]
            rsiIndex2 = peaks[i + 1]
            if values[rsiIndex] <= values[rsiIndex2]:  #Should I have just "<" or "<=" here? 
                return False
        return True
            
    def peaks_sorted_low_to_high(values:list, peaks:list, nrOfPeaks=0):
        if nrOfPeaks == 0:
            nrOfPeaks = len(peaks)
        peaks.sort()
        peaks = peaks[-nrOfPeaks:]
        for i in range(len(values) - 1):
            rsiIndex = peaks[i]
            rsiIndex2 = peaks[i + 1]
            if values[rsiIndex] >= values[rsiIndex2]:  #Should I have just "<" or "<=" here? 
                return False
        return True

    def find_levels(values, peakIndexes) -> list[Level]:
        levels = []
        for i in peakIndexes:
            value = values[i]
            levelValues = [x for x in values if x < value * 1.05 and x > value * 0.95]
            if len(levelValues) <= 2:
                levels.append(Level(sum(levelValues) / len(levelValues), len(levelValues)))
        return levels