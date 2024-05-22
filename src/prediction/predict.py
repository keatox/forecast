from datetime import timedelta
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

stock = 'GOOG'

ticker = yf.Ticker(stock)

prices = pd.DataFrame()
prices[stock] = ticker.history(period='1y')['Close']

log_return = np.log(1 + prices.pct_change())
u = log_return.mean()
var = log_return.var()
drift = u - (0.5*var)

stdev = log_return.std()
days = 200
iters = 10000
Z = norm.ppf(np.random.rand(days, iters)) 
daily_returns = np.exp(drift.values + stdev.values * Z)

price_paths = np.zeros_like(daily_returns)
price_paths[0] = prices.iloc[-1]
for i in range(1, days):
    price_paths[i] = price_paths[i-1]*daily_returns[i]

prediction = price_paths.mean(axis=1)[-1]
print(prediction)

plt.figure(figsize=(15,6))
plt.plot(prices)
new_dates = [prices[stock].index[-1] + timedelta(days=i) for i in range(0,days)]
plt.plot(new_dates,price_paths[:,0:10])
plt.plot(new_dates,price_paths[:,0:10].mean(axis=1),label="ahh")
plt.legend()
plt.show()