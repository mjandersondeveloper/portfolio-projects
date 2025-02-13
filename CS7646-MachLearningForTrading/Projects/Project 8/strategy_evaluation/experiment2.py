import datetime as dt  	
import pandas as pd
import matplotlib.pyplot as plt

import StrategyLearner as sl
import marketsimcode as markism

class ExperimentTwo(object):  
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
    
    def plot_figure(self, title, y_label, save_filename):
        # Title
        plt.title(title) 

        # Labels
        plt.xlabel("Impact")
        plt.ylabel(y_label)

        # Save
        plt.savefig("./images/" + save_filename + ".png")
    
    def run(self, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
        impact_values = [0.00, 0.002, 0.05, 0.7, 1.00]
        strategy_learner_means = []
        trade_numbers = []
        
        for impact in impact_values:
            # Get strategy learner orders
            strategy_learner = sl.StrategyLearner(impact)
            strategy_learner.add_evidence(symbol, sd, ed, sv)
            strategy_learner_df = strategy_learner.testPolicy(symbol, sd, ed, sv)

            strategy_learner_order_table = self.create_order_table(symbol, strategy_learner_df)
            strategy_port_val = markism.compute_portvals(strategy_learner_order_table, start_val=sv, impact=impact)
            strategy_trade_orders = self.normalize_values(strategy_port_val)

            # Calculate metrics
            strategy_learner_daily_rets = strategy_trade_orders.pct_change().dropna()
            strategy_learner_mean = strategy_learner_daily_rets.mean()
            
            strategy_learner_means.append(strategy_learner_mean)
            trade_numbers.append(strategy_learner_order_table[strategy_learner_order_table["Order"] != 0].shape[0])
        
        # Plot metric one
        plt.figure()
        plt.plot(strategy_learner_means)
        plt.xticks(range(len(impact_values)), impact_values)        
        self.plot_figure("Experiment 2 - In-Sample Average Daily Returns", "Average Return", "figure_avg_rets")

        # Plot metric two
        plt.figure()
        plt.plot(trade_numbers)
        plt.xticks(range(len(impact_values)), impact_values)        
        self.plot_figure("Experiment 2 - In-Sample Number of Trades", "Number of Trades", "figure_number_trades")