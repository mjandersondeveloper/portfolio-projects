import datetime as dt  		  	   		  		 			  		 			     			  	  	   		  		 			  		 			     			  	 
import pandas as pd  
		  	   		  		 			  		 			     			  	 
from util import get_data

def author():  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
    return "manderson332"

def initialize_df(template_df):
    new_df = template_df.copy()
    new_df.iloc[:] = 0.0
    return new_df

def trading_simulator(trades_df, prices_df, symbol):
    first_trade = 1000 if prices_df.iloc[0,1] == "BUY" else -1000
    trades_df[symbol].iloc[0] = net_holdings = first_trade

    for date, row in prices_df[1:-1].iterrows():
        order = row["Order"]
        if order == "BUY" and net_holdings < 1000:
            if net_holdings == 0: # Checks for existing short/long shares
                trades_df.loc[date] = 1000
                net_holdings += 1000
            else:
                trades_df.loc[date] = 2000
                net_holdings += 2000
        elif order == "SELL" and net_holdings > -1000:
            if net_holdings == 0: # Checks for existing short/long shares
                trades_df.loc[date] = -1000
                net_holdings -= 1000
            else:
                trades_df.loc[date] = -2000
                net_holdings -= 2000

def testPolicy(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
    # Get dates
    dates = pd.date_range(sd, ed)

    # Get prices on trading days
    prices_df = get_data([symbol], dates)
    prices_df = prices_df[[symbol]]
    
    # Create trade dataframe
    trades_df = initialize_df(prices_df)

    # Calcuate difference and set buy/sell indicators
    prices_df["Order"] = prices_df.shift(-1) > prices_df
    prices_df["Order"] = prices_df["Order"].apply(lambda x: "BUY" if x == True else "SELL") # https://sparkbyexamples.com/pandas/pandas-apply-with-lambda-examples/

    # Start trading
    trading_simulator(trades_df, prices_df, symbol)

    return trades_df
