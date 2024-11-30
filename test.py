import yfinance as yf
from Datapoint import Datapoint
from Calculator import Calculator

msft = yf.Ticker("QQQ")

hist = msft.history(period="1mo", interval="1h")

#print(hist)

#for index, value in hist.iterrows():
#   print(index) 
#   print(value['Close'])



prices = [100, 101, 100.5, 101.5, 101, 102, 101.5, 102.5, 102, 103, 102.5, 103.5, 103, 103]
datapoints: list[Datapoint] = []
for x in prices:
   dp = Datapoint(x, 1)
   if len(datapoints) > 0:
       dp.calc_loss_gains(datapoints[-1])
   datapoints.append(dp) 

for x in datapoints:
    print(str(x))

rsi = Calculator.calulate_rsi(datapoints, 0, 0)
print(rsi)
