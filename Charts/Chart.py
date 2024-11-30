from datetime import datetime
from datetime import timezone
class Chart:
    def __init__(self):


    def isExactTime():
    
    def convert_timestamp(self, timestamp_ms):
        timestamp_s = timestamp_ms / 1000
        date_time = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
        return date_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_chart_time():
        #Move get_chart_time function from stock class to in here. Make a classes called, hourly, minute and so on that implements different get_chart_time methods
