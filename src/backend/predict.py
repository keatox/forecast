from datetime import timedelta
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.express as px
import plotly.graph_objects as go
from jinja2 import Template

class Predict:
    def __init__(self):
        self.__prices = None
        self.__tickers = np.loadtxt('res/nasdaq.csv',skiprows=1,usecols=(0,1,5,6,8,9),dtype=str,delimiter=',')

    def predict_prices(self,stock,days=85,iters=10000):
        price_paths = self.compute_returns(stock,days,iters)
        prediction = price_paths.mean(axis=1)[-1]
        print(f'Og price: ${self.__prices.iloc[-days].values[0]}')
        print(f"Predicted: ${prediction}")
        print(f"Actual: ${self.__prices.iloc[-1].values[0]}")
        print('Percent Change: %.2f' % float(100 * ((prediction - self.__prices.iloc[-days])/self.__prices.iloc[-days]).values[0])+'%')

        from sklearn.metrics import mean_absolute_error, mean_squared_error
        mae = mean_absolute_error(self.__prices.iloc[-days-1:-1], price_paths.mean(axis=1))
        mse = mean_squared_error(self.__prices.iloc[-days-1:-1], price_paths.mean(axis=1))
        rmse = np.sqrt(mse)
        print(f'Mean Absolute Error (MAE): {mae}')
        print(f'Mean Squared Error (MSE): {mse}')
        print(f'Root Mean Squared Error (RMSE): {rmse}')

        plt = px.line(self.__prices)

        new_dates = [self.__prices[stock].index[-days] + timedelta(days=i) for i in range(0,days)]
        num_graphs = 0
        for i in range(len(price_paths)):
            if num_graphs < 3 and abs(price_paths[:,i][-1] - prediction) <= 0.1 * prediction:
                plt.add_trace(go.Scatter(x=new_dates, y=price_paths[:,i],mode='lines',opacity=0.35))
                num_graphs += 1
        plt.add_vline(x=self.__prices[stock].index[-days],line_color='gray',line_dash='dash')
        plt.update_layout(showlegend=False,
                          yaxis_title=None,
                          xaxis_title=None,
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=20, r=20, t=20, b=20),
                          autosize=True)

        plt.show()
        
        return {'chart': plt.to_html(full_html=False,config={'displayModeBar': False}),
                'initial': 5,
                'predicted': 7,
               }

    def get_prices(self,stock):
        ticker = yf.Ticker(stock)
        prices = pd.DataFrame()
        prices[stock] = ticker.history(period='1y')['Close']
        self.__prices = prices

    def compute_returns(self,stock,days,iters):
        self.get_prices(stock)
        log_return = np.log(1 + self.__prices.pct_change())
        u = log_return.mean()
        var = log_return.var()
        drift = u - (0.5*var)
        stdev = log_return.std()

        rng = np.random.default_rng()
        Z = norm.ppf(rng.uniform(size=(days, iters)))
        daily_returns = np.exp(drift.values + stdev.values * Z)

        price_paths = np.zeros_like(daily_returns)
        price_paths[0] = self.__prices.iloc[-days]
        for i in range(1, days):
            price_paths[i] = price_paths[i-1]*daily_returns[i]
        return price_paths

stock = 'NVDA'
model = Predict()
model.predict_prices(stock,90)