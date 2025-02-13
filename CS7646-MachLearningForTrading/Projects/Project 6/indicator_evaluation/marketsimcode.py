""""""  		  	   		  		 			  		 			     			  	 
"""MC2-P1: Market simulator.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  		 			  		 			     			  	 
All Rights Reserved  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			     			  	 
or edited.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			     			  	 
GT honor code violation.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Student Name: Marcus Anderson (replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: manderson332 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 903648648 (replace with your GT ID) 		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	   		 			  		 			     			  	 
import pandas as pd  		  	   		  		 			  		 			     			  	 
from util import get_data, plot_data
  		  	   		  		 			  		 			     			  	 
def author():  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
    return "manderson332"  # replace tb34 with your Georgia Tech username.   		  	   		  		 			  		 			     			  	 

def initialize_df(template_df):
    new_df = template_df.copy()
    new_df.iloc[:] = 0.0
    return new_df

def trade_simulator(trades_df, prices_df, orders_df, commission, impact):
    for date, row in orders_df.iterrows():
        order, symbol, shares = row["Order"], row["Symbol"], row["Shares"]
        
        share_order = shares
        if order == "SELL":
            share_order = -shares
        
        trades_df.loc[date, symbol] += share_order
        share_price = prices_df.loc[date, symbol]
        
        # Deduct/add to cashflow
        entry_exit_price = share_order * share_price
        transaction_costs = commission + abs(entry_exit_price * impact)

        trades_df.loc[date, "CASH"] -= entry_exit_price + transaction_costs

def calculate_holdings(holdings_df, trades_df):
    holdings_df.iloc[0,:] += trades_df.iloc[0,:]
    for date in range(1,len(holdings_df.index)):
        holdings_df.iloc[date,:] += holdings_df.iloc[date-1,:] + trades_df.iloc[date,:]

def compute_portvals(orders_df, start_val=100000, commission=0.00, impact=0.00):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Computes the portfolio values.  		  	   		  		 			  		 			     			  	 		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # Get start and end dates
    orders_df.sort_index(inplace=True)
    start_date = orders_df.index[0]
    end_date = orders_df.index[-1]
    dates = pd.date_range(start_date, end_date)

    # Get symbols
    symbols = orders_df["Symbol"].unique()

    # Get prices on trading days and add "CASH"
    prices_df = get_data(symbols, dates)
    prices_df = prices_df[symbols]
    prices_df["CASH"] = 1.0

    # Start trading
    trades_df = initialize_df(prices_df)
    trade_simulator(trades_df, prices_df, orders_df, commission, impact)
    
    # Create holdings
    holdings_df = initialize_df(trades_df)
    holdings_df.loc[start_date, "CASH"] = start_val
    calculate_holdings(holdings_df, trades_df)
    
    # Calculate stocks and portvals
    values_df = initialize_df(holdings_df)
    values_df =  prices_df * holdings_df
    portvals = values_df.sum(axis=1)
      	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	   		  		 			  		 			     			  	 
    return portvals  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
