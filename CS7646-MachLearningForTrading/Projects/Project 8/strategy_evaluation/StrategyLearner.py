""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
import random  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import pandas as pd  		  	   		  		 			  		 			     			  	 
import util as ut
import numpy as np

import BagLearner as bl
import RTLearner as rtl
import indicators as ind
 	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
class StrategyLearner(object):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 			  		 			     			  	 
        If verbose = False your code should not generate ANY output.  		  	   		  		 			  		 			     			  	 
    :type verbose: bool  		  	   		  		 			  		 			     			  	 
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  		 			  		 			     			  	 
    :type impact: float  		  	   		  		 			  		 			     			  	 
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  		 			  		 			     			  	 
    :type commission: float  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # constructor  		  	   		  		 			  		 			     			  	 
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        Constructor method  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        self.verbose = verbose  		  	   		  		 			  		 			     			  	 
        self.impact = impact  		  	   		  		 			  		 			     			  	 
        self.commission = commission 
        self.learner = bl.BagLearner(learner = rtl.RTLearner, kwargs = { "leaf_size" : 5 }, bags = 20)
        
        self.window_size = 19
        self.N = 10 # Day return
  	   		  		 			  		 			     			  	 
    def author(self):  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
        return "manderson332"
    
    def initialize_df(self, template_df):
        new_df = template_df.copy()
        new_df.iloc[:] = 0.0
        return new_df

    def get_indicator_values(self, prices, symbol):
         # Get indicator values - %B indicator, PPO indicator, MACD indicator
        percent_b = ind.percent_b_indicator(prices, symbol)
        ppo = ind.ppo_indicator(prices, symbol)
        macd = ind.macd_indicator(prices, symbol)

        # Combine indicator values and filter by window size
        combined_ind_df = pd.concat([percent_b, ppo, macd], axis=1)
        ind_values_df = combined_ind_df.iloc[self.window_size:]

        return ind_values_df[symbol].values
    
    def get_train_y(self, prices, symbol):
        train_y = np.asarray([])
        y_threshold = self.impact * 2
        for i in range(self.window_size, len(prices) - self.N):
            ret = (prices[symbol].iloc[i + self.N]/prices[symbol].iloc[i]) - 1.0
            if ret > y_threshold:
                train_y = np.append(train_y, 1)
            elif ret < -y_threshold:
                train_y = np.append(train_y, -1)
            else:
                train_y = np.append(train_y, 0)
        return train_y
    
    def build_orders(self, symbol, trade_orders_table): 
        trade_orders = self.initialize_df(trade_orders_table)
        net_holdings = 0
        
        for date, row in trade_orders_table.iterrows():
            order = row[symbol]
            if order == "BUY" and net_holdings < 1000:
                trade_size = 1000 if net_holdings == 0 else 2000
                trade_orders.loc[date] = trade_size
                net_holdings += trade_size
            elif order == "SELL" and net_holdings > -1000:
                trade_size = -1000 if net_holdings == 0 else -2000
                trade_orders.loc[date]  = trade_size
                net_holdings += trade_size
        return trade_orders
    
    # this method should create a QLearner, and train it for trading  		  	   		  		 			  		 			     			  	 
    def add_evidence(self, symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=10000):  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        Trains your strategy learner over a given time frame.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        :param symbol: The stock symbol to train on  		  	   		  		 			  		 			     			  	 
        :type symbol: str  		  	   		  		 			  		 			     			  	 
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 			  		 			     			  	 
        :type sd: datetime  		  	   		  		 			  		 			     			  	 
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 			  		 			     			  	 
        :type ed: datetime  		  	   		  		 			  		 			     			  	 
        :param sv: The starting value of the portfolio  		  	   		  		 			  		 			     			  	 
        :type sv: int  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 	   		  		 			  		 			     			  	   		  		 			  		 			     			  	 
        # Get prices
        dates = pd.date_range(sd, ed)  		  	   		  		 			  		 			     			  	 
        prices_all = ut.get_data([symbol], dates)		  	   		  		 			  		 			     			  	 
        prices = prices_all[[symbol]]

        # Get train_x values
        train_x = self.get_indicator_values(prices, symbol)
        train_x = np.asarray(train_x[:len(train_x) - self.N])
        
        # Get train_y values
        train_y = self.get_train_y(prices, symbol)

        # Add evidence to RTLearner
        self.learner.add_evidence(train_x, train_y)  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # this method should use the existing policy and test it against new data  		  	   		  		 			  		 			     			  	 
    def testPolicy(self, symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=10000):  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        Tests your learner using data outside of the training data  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        :param symbol: The stock symbol that you trained on on  		  	   		  		 			  		 			     			  	 
        :type symbol: str  		  	   		  		 			  		 			     			  	 
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 			  		 			     			  	 
        :type sd: datetime  		  	   		  		 			  		 			     			  	 
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 			  		 			     			  	 
        :type ed: datetime  		  	   		  		 			  		 			     			  	 
        :param sv: The starting value of the portfolio  		  	   		  		 			  		 			     			  	 
        :type sv: int  		  	   		  		 			  		 			     			  	 
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		  		 			  		 			     			  	 
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		  		 			  		 			     			  	 
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		  		 			  		 			     			  	 
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		  		 			  		 			     			  	 
        :rtype: pandas.DataFrame  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 	   		  		 			  		 			     			  	 		  	   		  		 			  		 			     			  	 
        # Get prices
        dates = pd.date_range(sd, ed)  		  	   		  		 			  		 			     			  	 
        prices_all = ut.get_data([symbol], dates)		  	   		  		 			  		 			     			  	 
        prices = prices_all[[symbol]]
        
        # Run RTLearner query for test_x values
        test_x = self.get_indicator_values(prices, symbol)
        
        # Get predy data
        pred_y = self.learner.query(test_x)
        
        # Create trade table
        trades_df = self.initialize_df(prices.iloc[self.window_size:])
        trades_df[symbol] = pred_y
        trades_df[symbol] = trades_df[symbol].apply(lambda x: "BUY" if x > 0.5 else "SELL" if x < -0.5 else 0)

        # Build trade orders
        trade_orders = self.build_orders(symbol, trades_df)
        
        return trade_orders 		  	   		  		 			  		 			     			  	   	   		  		 			  		 			     			  	   		  	   		  		 			  		 			     			  	