""""""  		  	   		  		 			  		 			     			  	 
"""MC1-P2: Optimize a portfolio.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
  		  	   		  		 			  		 			     			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: tb34 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import datetime as dt  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np 
import scipy.optimize as spo
  		  	   		  		 			  		 			     			  	 
import matplotlib.pyplot as plt  		  	   		  		 			  		 			     			  	 
import pandas as pd  		  	   		  		 			  		 			     			  	 
from util import get_data, plot_data  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
# This is the function that will be tested by the autograder  		  	   		  		 			  		 			     			  	 
# The student must update this code to properly implement the functionality  		  	   		  		 			  		 			     			  	 
def optimize_portfolio(  		  	   		  		 			  		 			     			  	 
    sd=dt.datetime(2008, 1, 1),  		  	   		  		 			  		 			     			  	 
    ed=dt.datetime(2009, 1, 1),  		  	   		  		 			  		 			     			  	 
    syms=["GOOG", "AAPL", "GLD", "XOM"],  		  	   		  		 			  		 			     			  	 
    gen_plot=False,  		  	   		  		 			  		 			     			  	 
):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe  		  	   		  		 			  		 			     			  	 
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of  		  	   		  		 			  		 			     			  	 
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take  		  	   		  		 			  		 			     			  	 
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and  		  	   		  		 			  		 			     			  	 
    statistics.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 			  		 			     			  	 
    :type sd: datetime  		  	   		  		 			  		 			     			  	 
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 			  		 			     			  	 
    :type ed: datetime  		  	   		  		 			  		 			     			  	 
    :param syms: A list of symbols that make up the portfolio (note that your code should support any  		  	   		  		 			  		 			     			  	 
        symbol in the data directory)  		  	   		  		 			  		 			     			  	 
    :type syms: list  		  	   		  		 			  		 			     			  	 
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your  		  	   		  		 			  		 			     			  	 
        code with gen_plot = False.  		  	   		  		 			  		 			     			  	 
    :type gen_plot: bool  		  	   		  		 			  		 			     			  	 
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,  		  	   		  		 			  		 			     			  	 
        standard deviation of daily returns, and Sharpe ratio  		  	   		  		 			  		 			     			  	 
    :rtype: tuple  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Read in adjusted closing prices for given symbols, date range  		  	   		  		 			  		 			     			  	 
    dates = pd.date_range(sd, ed)  		  	   		  		 			  		 			     			  	 
    prices_all = get_data(syms, dates)  # automatically adds SPY  		  	   		  		 			  		 			     			  	 
    prices = prices_all[syms]  # only portfolio symbols  		  	   		  		 			  		 			     			  	 
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later 
	   		  		 			  		 			     			  	 
    # find the allocations for the optimal portfolio  		  	   		  		 			  		 			     			  	 
    # note that the values here ARE NOT meant to be correct for a test case  	  		 			  		 			     			  	 
    
    # Initial allocations
    allocs = np.ones(len(syms)) / len(syms)

    # Get normal value portfolio
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html
    normed_val = prices/prices.iloc[0]

    # Optimize Shape Ratio
    bound = [(0,1) for i in range(len(syms))]
    constraint = ({ "type": "ineq", "fun": lambda inputs: 1 - np.sum(inputs)}, { "type": "eq", "fun": lambda inputs: 1 - np.sum(inputs) })
    optimize = spo.minimize(negative_sharpe_ratio, allocs, args=(normed_val), bounds=bound, constraints=constraint)
    allocs = optimize.x

    # Get port_val and daily_return for statistic calculations
    port_val = get_portfolio_val(normed_val, allocs)
    daily_returns  = get_daily_val(port_val)

    # Compute statistics
    cr, adr, sddr, sr = calculate_stats(port_val, daily_returns)

    # Compare daily portfolio value with SPY using a normalized plot  		  	   		  		 			  		 			     			  	 
    if gen_plot:  		  	   		  		 			  		 			     			  	 
        # Normalize price_SPY data
        prices_SPY = prices_SPY/prices_SPY.iloc[0]

        # Data cleansing
        port_val.fillna(method='ffill', inplace=True)
        port_val.fillna(method='bfill', inplace=True)

        prices_SPY.fillna(method='ffill', inplace=True)
        prices_SPY.fillna(method='bfill', inplace=True)

        # Plot
        df_temp = pd.concat([port_val, prices_SPY], keys=["Portfolio", "SPY"], axis=1) 
        df_temp.plot(kind="line")

        plt.title("Daily Portfolio Value and SPY")    
        plt.xlabel("Date")
        plt.ylabel("Normalized Price")

        plt.legend(["Portfolio", "SPY"])
        plt.savefig("./images/Figure1.png")
        
        pass  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    return allocs, cr, adr, sddr, sr  		  	   		  		 			  		 			     			  	 

def get_portfolio_val(n_p, a):
    allocated_val = n_p * a
    pos_val = allocated_val * 1

    return pos_val.sum(axis=1)	 
    
def get_daily_val(pv):
    # Compute daily returns
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html 
    return pv.pct_change().dropna()

def calculate_stats(pv, dr):
    cr = (pv.iloc[-1]/pv.iloc[0]) - 1
    adr = np.mean(dr)
    sddr = np.std(dr)
    sr = sharpe_ratio(adr, sddr)

    return np.asarray([cr, adr, sddr, sr])

def sharpe_ratio(adr, sddr, rf=0.0): 
    sr = (adr - rf) / sddr
    asr = (252**(1/2)) * sr

    return asr
    
def negative_sharpe_ratio(allocs, norm_prices): 
    port_val = get_portfolio_val(norm_prices, allocs)
    daily_returns = get_daily_val(port_val)

    # Return sharpe ratio
    adr = np.mean(daily_returns)
    sddr = np.std(daily_returns)
    sr = sharpe_ratio(adr, sddr)

    return -sr
  		  	   		  		 			  		 			     			  	 
def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    This function WILL NOT be called by the auto grader.  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    start_date = dt.datetime(2008, 6, 1)  		  	   		  		 			  		 			     			  	 
    end_date = dt.datetime(2009, 6, 1)  		  	   		  		 			  		 			     			  	 
    symbols =  ["IBM", "X", "GLD", "JPM"]	  	   		  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Assess the portfolio  		  	   		  		 			  		 			     			  	 
    allocations, cr, adr, sddr, sr = optimize_portfolio(  		  	   		  		 			  		 			     			  	 
        sd=start_date, ed=end_date, syms=symbols, gen_plot=False  		  	   		  		 			  		 			     			  	 
    )  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Print statistics  		  	   		  		 			  		 			     			  	 
    print(f"Start Date: {start_date}")  		  	   		  		 			  		 			     			  	 
    print(f"End Date: {end_date}")  		  	   		  		 			  		 			     			  	 
    print(f"Symbols: {symbols}")  		  	   		  		 			  		 			     			  	 
    print(f"Allocations:{allocations}")  		  	   		  		 			  		 			     			  	 
    print(f"Sharpe Ratio: {sr}")  		  	   		  		 			  		 			     			  	 
    print(f"Volatility (stdev of daily returns): {sddr}")  		  	   		  		 			  		 			     			  	 
    print(f"Average Daily Return: {adr}")  		  	   		  		 			  		 			     			  	 
    print(f"Cumulative Return: {cr}")  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    # This code WILL NOT be called by the auto grader  		  	   		  		 			  		 			     			  	 
    # Do not assume that it will be called  		  	   		  		 			  		 			     			  	 
    test_code()  		  	   		  		 			  		 			     			  	 
