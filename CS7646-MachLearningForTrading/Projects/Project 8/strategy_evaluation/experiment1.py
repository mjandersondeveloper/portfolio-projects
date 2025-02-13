import datetime as dt  	
import pandas as pd

from util import get_data

import ManualStrategy as ms
import StrategyLearner as sl
import marketsimcode as markism

class ExperimentOne(object):  
    def author(self):  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
        return "manderson332"

    def create_order_table(self, symbol, trade_data):
        trade_orders = pd.DataFrame(index=trade_data.index)
        
        trade_orders["Symbol"] = symbol
        trade_orders["Order"] = trade_data[symbol].apply(lambda x: "BUY" if x > 0 else "SELL" if x < 0 else 0)
        trade_orders["Shares"] = abs(trade_data)
        
        return trade_orders
    
    def normalize_values(self, df):
        return df/df.iloc[0]
    
    def run(self, symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
        # Get manual strategy orders
        manual_strategy = ms.ManualStrategy()
        manual_strategy_df = manual_strategy.testPolicy(symbol, sd, ed, sv)

        manual_strategy_order_table = self.create_order_table(symbol, manual_strategy_df)
        manual_port_val = markism.compute_portvals(manual_strategy_order_table, start_val=sv, commission=9.95, impact=0.005)
        manual_trade_orders = self.normalize_values(manual_port_val)
        
        # Get strategy learner orders
        strategy_learner = sl.StrategyLearner(impact=0.005, commission=9.95)
        strategy_learner.add_evidence(symbol, sd, ed, sv)
        strategy_learner_df = strategy_learner.testPolicy(symbol, sd, ed, sv)

        strategy_learner_order_table = self.create_order_table(symbol, strategy_learner_df)
        strategy_port_val = markism.compute_portvals(strategy_learner_order_table, start_val=sv, commission=9.95, impact=0.005)
        strategy_trade_orders = self.normalize_values(strategy_port_val)

        # Get benchmark orders
        prices_all = get_data([symbol], pd.date_range(sd, ed))
        prices = prices_all[[symbol]]
        
        benchmark_df = pd.DataFrame(index=prices.index)
        benchmark_df["Symbol"], benchmark_df["Order"], benchmark_df["Shares"]  = symbol, 0, 0
        benchmark_df.iloc[0,1] = "BUY"
        benchmark_df.iloc[0,2] = 1000

        benchmark_port_val = markism.compute_portvals(benchmark_df, start_val=sv, commission=9.95, impact=0.005)
        benchmark_trade_orders = self.normalize_values(benchmark_port_val)

        return manual_trade_orders, strategy_trade_orders, benchmark_trade_orders

