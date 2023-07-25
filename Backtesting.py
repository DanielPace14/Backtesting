import pandas_datareader as pdr
from datetime import datetime
from datetime import timedelta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()
def EMA(values, n):
    return pd.Series(values).ewm(span=n,min_periods=0, adjust=False).mean()
def RSI(array, n=14):
    gain = pd.Series(array).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.ewm(span=n,min_periods=0,adjust=False).mean()/loss.abs().ewm(span=n,min_periods=0,adjust=False).mean()
    return 100 - 100 / (1 + rs)
    
class SMAC(Strategy):
		def init(self):
			price = self.data.Close
			self.sma1 = self.I(SMA, price, 10)
			self.sma2 = self.I(SMA, price, 20)
		def next(self):
			if crossover(self.sma1, self.sma2):
				self.buy()
			elif crossover(self.sma2, self.sma1):
				self.sell()
class EMAC(Strategy):
    def init(self):
        price = self.data.Close
        self.ema1 = self.I(EMA, price, 7)
        self.ema2 = self.I(EMA, price, 27)
        self.ema3 = self.I(EMA, price, 200)
    def next(self):
        if crossover(self.ema1, self.ema3):
            self.buy()
        elif crossover(self.ema3, self.ema1) and crossover(self.ema2, self.ema1):
            self.sell()

class RSISystem(Strategy):
     def init(self):
         price= self.data.Close
         self.RSIData = self.I(RSI,price,14)
         self.ema3 = self.I(EMA, price, 5)
         self.ema4 = self.I(EMA, price, 10)
     def next(self):
         if not self.position and self.RSIData<30 and crossover(self.ema4, self.ema3):    
            self.buy()
         elif self.RSIData>70 and crossover(self.ema3, self.ema4):
            if self.position.size>0:
                self.position.close()

# stock = pdr.get_data_yahoo(symbols='SPY', start = datetime.today()-timedelta(days=3652), end =datetime.today())
stock = pdr.get_data_yahoo(symbols='SPY', start = '2011-12-1', end ='2021-12-1')

bt = Backtest(stock, EMAC,cash=10000, commission = 0.000,
    exclusive_orders= True)

print(bt.run())