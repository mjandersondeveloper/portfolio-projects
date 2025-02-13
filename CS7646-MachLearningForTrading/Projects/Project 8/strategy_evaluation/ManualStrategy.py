import datetime as dt  	
import pandas as pd

from util import get_data

import indicators as ind

class ManualStrategy(object):  		  	   		  		 			  		 			     			  	
    def author(self):  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
        return "manderson332"

    def initialize_df(self, template_df):
        new_df = template_df.copy()
        new_df.iloc[:] = 0.0
        return new_df

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
                trade_orders.loc[date] = trade_size
                net_holdings += trade_size
        return trade_orders

    def testPolicy(self, symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
        # Get dates
        dates = pd.date_range(sd, ed)

        # Get prices on trading days
        prices_df = get_data([symbol], dates)
        prices = prices_df[[symbol]]

        # Get indicator signals - %B indicator, PPO indicator, MACD indicator
        percent_b_signals = ind.percent_b_indicator(prices, symbol, return_signals=True)
        ppo_signals = ind.ppo_indicator(prices, symbol, return_signals=True)
        macd_signals = ind.macd_indicator(prices, symbol, return_signals=True)

        # Combine signal values
        trade_signals = percent_b_signals + ppo_signals + macd_signals

        # Create trade table
        trades_df = self.initialize_df(prices)
        trades_df[symbol] = trade_signals
        trades_df[symbol] = trades_df[symbol].apply(lambda x: "BUY" if x > 1 else "SELL" if x < -1 else 0)
        
        # Build trade orders
        trade_orders = self.build_orders(symbol, trades_df)

        return trade_orders