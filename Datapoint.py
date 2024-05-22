

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