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
import datetime as dt  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import pandas as pd  		  	   		  		 			  		 			     			  	 
from util import get_data, plot_data
  		  	   		  		 			  		 			     			  	 
def author():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT username of the student  		  	   		  		 			  		 			     			  	 
    :rtype: str  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
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
        holdings_df.iloc[date,:] += holdings_df.iloc[date-1,:] + trades_df.iloc[date,:] # https://stackoverflow.com/questions/34855859/is-there-a-way-in-pandas-to-use-previous-row-value-in-dataframe-apply-when-previ

def compute_portvals(orders_file="./orders/orders.csv", start_val=1000000, commission=9.95, impact=0.005):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Computes the portfolio values.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param orders_file: Path of the order file or the file object  		  	   		  		 			  		 			     			  	 
    :type orders_file: str or file object  		  	   		  		 			  		 			     			  	 
    :param start_val: The starting value of the portfolio  		  	   		  		 			  		 			     			  	 
    :type start_val: int  		  	   		  		 			  		 			     			  	 
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		  		 			  		 			     			  	 
    :type commission: float  		  	   		  		 			  		 			     			  	 
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		  		 			  		 			     			  	 
    :type impact: float  		  	   		  		 			  		 			     			  	 
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		  		 			  		 			     			  	 
    :rtype: pandas.DataFrame  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # this is the function the autograder will call to test your code  		  	   		  		 			  		 			     			  	 
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		  		 			  		 			     			  	 
    # code should work correctly with either input  		  	   		  		 			  		 			     			  	 
    # TODO: Your code here  
    orders_df = pd.read_csv(orders_file, index_col="Date", parse_dates=True, na_values=["nan"])
    
    # Get start and end dates
    orders_df.sort_index(inplace=True) # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_index.html
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
  		  	   		  		 			  		 			     			  	 
def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Helper function to test code  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # this is a helper function you can use to test your code  		  	   		  		 			  		 			     			  	 
    # note that during autograding his function will not be called.  		  	   		  		 			  		 			     			  	 
    # Define input parameters  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    of = "./orders/orders-02.csv"  		  	   		  		 			  		 			     			  	 
    sv = 1000000  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Process orders  		  	   		  		 			  		 			     			  	 
    portvals = compute_portvals(orders_file=of, start_val=sv)  		  	   		  		 			  		 			     			  	 
    if isinstance(portvals, pd.DataFrame):  		  	   		  		 			  		 			     			  	 
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		  		 			  		 			     			  	 
    else:  		  	   		  		 			  		 			     			  	 
        "warning, code did not return a DataFrame"  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Get portfolio stats  		  	   		  		 			  		 			     			  	 
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		  		 			  		 			     			  	 
    start_date = dt.datetime(2008, 1, 1)  		  	   		  		 			  		 			     			  	 
    end_date = dt.datetime(2008, 6, 1) 		  	   		  		 			  		 			     			  	 
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2, 0.01, 0.02, 1.5]  		  	   		  		 			  		 			     			  	   	   		  		 			  		 			     			  	 
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2, 0.01, 0.02, 1.5]  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Compare portfolio against $SPX  		  	   		  		 			  		 			     			  	 
    print(f"Date Range: {start_date} to {end_date}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		  		 			  		 			     			  	 
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		  		 			  		 			     			  	 
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		  		 			  		 			     			  	 
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		  		 			  		 			     			  	 
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Final Portfolio Value: {portvals[-1]}")  		  	   		  		 			  		 			     			  	 
                                                                            
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    test_code()  		  	   		  		 			  		 			     			  	 
