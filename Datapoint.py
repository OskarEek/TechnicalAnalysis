import pytz
from datetime import datetime


class Datapoint:

    def __init__(self, price, timeStamp, changePercentage=0, minPrice=0, maxPrice=0, rsi=0):

        self.min_price = minPrice if not minPrice == 0 else price
        self.max_price = maxPrice if not maxPrice == 0 else price
        self.price = price
        self.change_percentage = changePercentage
        self.loss = 0
        self.gain = 0
        self.rsi = rsi
        self.timestamp = timeStamp

    def calc_loss_gains(self, previousDp: 'Datapoint'):
        price_change = self.price - previousDp.price
        self.change_percentage = price_change / previousDp.price
        self.gain = price_change if price_change > 0 else 0
        self.loss = abs(price_change) if price_change < 0 else 0

    
    def timestamp_est(self):
        timestamp_s = self.timestamp / 1000
        # Create a timezone-aware datetime object in UTC
        utc_dt = datetime.fromtimestamp(timestamp_s, tz=pytz.utc)
        # Convert the datetime object to EST (Eastern Standard Time)
        est = pytz.timezone('America/New_York')
        est_dt = utc_dt.astimezone(est)

        # Return the formatted string based on the chart format
        return est_dt.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        string: str = "price: " + str(self.price) + "\n"
        string += "min price: " + str(self.min_price) + "\n"
        string += "max prce: " + str(self.max_price) + "\n"
        string += "change precentage: " + str(self.change_percentage) + "\n"
        string += "loss: " + str(self.loss) + "\n"
        string += "gain: " + str(self.gain) + "\n"
        string += "rsi: " + str(self.rsi) + "\n"
        string += "timestamp: " + str(self.timestamp) + "\n"
        return string

       


