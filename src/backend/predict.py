from datetime import timedelta
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
from datascraping import Datascraping

scraper = Datascraping()

#add error handling for invalid stock etc
stock = 'AAPL'

ticker = yf.Ticker(stock)

prices = pd.DataFrame()
prices[stock] = ticker.history(period='1y')['Close']

log_return = np.log(1 + prices.pct_change())
u = log_return.mean()
var = log_return.var()
drift = u - (0.5*var)

stdev = log_return.std()
days = 85
iters = 10000
Z = norm.ppf(np.random.rand(days, iters)) 
daily_returns = np.exp(drift.values + stdev.values * Z)

price_paths = np.zeros_like(daily_returns)
price_paths[0] = prices.iloc[-60]
for i in range(1, days):
    price_paths[i] = price_paths[i-1]*daily_returns[i]

prediction = price_paths.mean(axis=1)[-1]
print(f'Og price: ${prices.iloc[-60].values[0]}')
print(f"Predicted: ${prediction}")
print(f"Actual: ${prices.iloc[-1].values[0]}")
print('Percent Change: %.2f' % float(100 * ((prediction - prices.iloc[-60])/prices.iloc[-60]).values[0])+'%')

from sklearn.metrics import mean_absolute_error, mean_squared_error

mae = mean_absolute_error(prices.iloc[-days-1:-1], price_paths.mean(axis=1))
mse = mean_squared_error(prices.iloc[-days-1:-1], price_paths.mean(axis=1))
rmse = np.sqrt(mse)

print(f'Mean Absolute Error (MAE): {mae}')
print(f'Mean Squared Error (MSE): {mse}')
print(f'Root Mean Squared Error (RMSE): {rmse}')

plt.figure(figsize=(15,6))
plt.plot(prices)
new_dates = [prices[stock].index[-60] + timedelta(days=i) for i in range(0,days)]
num_graphs = 3
for i in range(len(price_paths)):
    if num_graphs <= 5 and abs(price_paths[:,i][-1] - prediction) <= prediction/(prediction // 10):
        plt.plot(new_dates,price_paths[:,i],alpha=0.35)
        num_graphs += 1
plt.show()