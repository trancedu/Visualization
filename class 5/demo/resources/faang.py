import pandas as pd
import yfinance as yf

#%% yfinance
class faangs():
    
    tickers = ['FB', 'AAPL', 'AMZN', 'NFLX', 'GOOG']
    data = pd.DataFrame()
    
    def __init__(self, period = 'max'):
        for ticker in self.tickers:
            myTicker = yf.Ticker(ticker)
            df = myTicker.history(period = period).reset_index()
            df['Date'] = pd.to_datetime(df['Date'], errors = 'coerce')
            
            # generate the growth rates
            for col in df.columns:
                if col not in ['Date']:
                    df[col + '_g'] = df[col].shift(-1) / df[col] - 1 
            
            # add the name
            df['Stock'] = ticker
            
            self.data = self.data.append(df)

if __name__ == '__main__':
    o = faangs()
    o.data

        