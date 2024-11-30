from datetime import datetime, timezone
import pytz

class DataDto:
    def __init__(self, data: dict):
        self.id: str = data['id']
        self.exchange: str = data['exchange']
        self.quoteType: int = data['quoteType'] 
        self.price: float = data['price']
        self.timestamp: int = data['timestamp']
        self.marketHours: int = data['marketHours']
        self.changePercent: float = data['changePercent']
        self.dayVolume: int = data['dayVolume']
        self.change: float = data['change']
        self.priceHint: int = data['priceHint']
