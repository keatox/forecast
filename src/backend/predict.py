from datetime import timedelta
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.express as px
import plotly.graph_objects as go

class Predict:
    def __init__(self):
        self.__prices = None
        self.info = None

    # returns predicted prices in graph and numerical form
    def predict_prices(self,stock,days=90,iters=10000):
        info = self.get_prices(stock)
        price_paths = self.compute_returns(days,iters)
        prediction = price_paths.mean(axis=1)[-1]

        # can be used to test accuracy of model
        """
        from sklearn.metrics import mean_absolute_error, mean_squared_error
        mae = mean_absolute_error(self.__prices.iloc[-days-1:-1], price_paths.mean(axis=1))
        mse = mean_squared_error(self.__prices.iloc[-days-1:-1], price_paths.mean(axis=1))
        rmse = np.sqrt(mse)
        print(f'Mean Absolute Error (MAE): {mae}')
        print(f'Mean Squared Error (MSE): {mse}')
        print(f'Root Mean Squared Error (RMSE): {rmse}')
        """

        # graph instantiation
        plt = px.line(self.__prices)

        new_dates = [self.__prices[''].index[-1] + timedelta(days=i) for i in range(0,days)]
        num_graphs = 0
        for i in range(len(price_paths)):
            if num_graphs < 3 and abs(price_paths[:,i][-1] - prediction) <= 0.1 * prediction:
                plt.add_trace(go.Scatter(x=new_dates, y=price_paths[:,i],mode='lines',opacity=0.35))
                num_graphs += 1
        plt.add_vline(x=self.__prices[''].index[-1],line_color='rgba(211,211,211,0.25)',line_dash='dash')
        plt.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        plt.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
        plt.update_layout(showlegend=False,
                          yaxis_title=None,
                          yaxis=dict(color="rgba(238,153,0,0.75)"),
                          xaxis_title=None,
                          xaxis=dict(color="rgba(238,153,0,0.75)"),
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=20, r=20, t=20, b=20),
                          autosize=True)

        info.update({'chart': plt.to_html(full_html=False,config={'displayModeBar': False, 'scrollZoom': True}),
                     'initial': '%.2f' % self.__prices.iloc[-1].values[0],
                     'predicted': '%.2f' % prediction,
                     'change': '%.2f' % float(100 * ((prediction - self.__prices.iloc[-1])/self.__prices.iloc[-1]).values[0])})
        self.info = info
    
    # returns abbreviation of large numbers
    def condense_num(self,num):
        if num == 'N/A':
            return 'N/A'
        if num <= 1000:
            return num
        elif num < 1000000:
            return '%.2fK' % (num/1000) 
        elif num < 1000000000:
            return '%.2fM' % (num/1000000)
        elif num < 1000000000000:
            return '%.2fB' % (num/1000000000) 
        else: 
            return '%.2fT' % (num/1000000000000) 
    
    # queries yfinance to get relevant stock data
    def get_prices(self,stock):
        ticker = yf.Ticker(stock)
        prices = pd.DataFrame()
        hist = ticker.history(period='1y')['Close']
        if len(hist) <= 0:
            prices[''] = ticker.history(period='max')['Close']
        else:
            prices[''] = hist
        self.__prices = prices
        info = ticker.info
        return {'fullname': info.get('shortName','N/A'),
                'country': info.get('country','N/A'),
                'sector': info.get('sector','N/A'),
                'industry': info.get('industry','N/A'),
                'volume': self.condense_num(info.get('volume','N/A')),
                'markcap': self.condense_num(info.get('marketCap','N/A')),
                'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow','N/A'), 
                'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh','N/A')}

    # simulate Brownian motion via Monte Carlo
    def compute_returns(self,days,iters):
        log_return = np.log(1 + self.__prices.pct_change())
        u = log_return.mean()
        var = log_return.var()
        drift = u - (0.5*var)
        stdev = log_return.std()

        rng = np.random.default_rng()
        Z = norm.ppf(rng.uniform(size=(days, iters)))
        daily_returns = np.exp(drift.values + stdev.values * Z)

        price_paths = np.zeros_like(daily_returns)
        price_paths[0] = self.__prices.iloc[-1]
        for i in range(1, days):
            price_paths[i] = price_paths[i-1]*daily_returns[i]
        return price_paths