import datetime as dt  	
import pandas as pd
import matplotlib.pyplot as plt

from util import get_data

import ManualStrategy as ms
import marketsimcode as markism
import experiment1
import experiment2

def author():  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
    return "manderson332"

def create_order_table(symbol, trade_data):
    trade_orders = pd.DataFrame(index=trade_data.index)
    
    trade_orders["Symbol"] = symbol
    trade_orders["Order"] = trade_data[symbol].apply(lambda x: "BUY" if x > 0 else "SELL" if x < 0 else 0)
    trade_orders["Shares"] = abs(trade_data)

    return trade_orders

def create_benchmark_orders(prices):
    benchmark_orders = pd.DataFrame(index=prices.index)
    benchmark_orders["Symbol"], benchmark_orders["Order"], benchmark_orders["Shares"]  = symbol, 0, 0
    benchmark_orders.iloc[0,1] = "BUY"
    benchmark_orders.iloc[0,2] = 1000

    return benchmark_orders

def calculate_statistics(benchmark_port_val, manual_strategy_port_val) :
    benchmark_daily_rets = benchmark_port_val.pct_change().dropna()
    port_val_daily_rets = manual_strategy_port_val.pct_change().dropna()

    # Benchmark statistics
    benchmark_cr = ((benchmark_port_val.iloc[-1]/benchmark_port_val.iloc[0]) - 1)
    benchmark_std = benchmark_daily_rets.std()
    benchmark_mean = benchmark_daily_rets.mean()
    
    # Portfolio statistics
    port_val_cr = ((manual_strategy_port_val.iloc[-1]/manual_strategy_port_val.iloc[0]) - 1)
    port_val_std = port_val_daily_rets.std()
    port_val_mean = port_val_daily_rets.mean()

    return pd.DataFrame(data=[["Benchmark", benchmark_cr, benchmark_std, benchmark_mean], ["Manual Strategy", port_val_cr, port_val_std, port_val_mean]], columns=["Portfolio Type", "Cumulative return", "Standard Deviation", "Mean"])

def normalize_values(df):
    return df/df.iloc[0]

def plot_figure(title, legend, save_filename):
    # Title
    plt.title(title) 

    # Labels
    plt.xlabel("Date")
    plt.ylabel("Normalized Price")
    plt.xticks(rotation=30)

    # Legend and save
    if legend: plt.legend(legend)
    plt.savefig("./images/" + save_filename + ".png")

if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    # Set variables
    symbol = "JPM"
    in_sample_sd, in_sample_ed = dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31)
    out_sample_sd, out_sample_ed = dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31)

    # Run manual strategy
    manual_strategy = ms.ManualStrategy()

    # Get in-sample data
    in_sample_trades = manual_strategy.testPolicy(symbol, sd=in_sample_sd, ed=in_sample_ed)

    # Create in-sample trade order table
    in_sample_trade_order_table = create_order_table(symbol, in_sample_trades)

    # Get normalized in-sample trade orders
    in_sample_port_val = markism.compute_portvals(in_sample_trade_order_table, commission=9.95, impact=0.005)
    in_sample_trade_orders = normalize_values(in_sample_port_val)

    # Get in-sample benchmark data
    prices_all = get_data([symbol], pd.date_range(in_sample_sd, in_sample_ed))
    prices = prices_all[[symbol]]
    
   # Create in-sample trade order table
    benchmark_in_sample_orders = create_benchmark_orders(prices)

    # Get normalized in-sample trade orders
    benchmark_in_sample_port_val = markism.compute_portvals(benchmark_in_sample_orders, commission=9.95, impact=0.005)
    benchmark_in_sample_trade_orders = normalize_values(benchmark_in_sample_port_val)

    # Set long/short entry points
    in_sample_short_long_points = in_sample_trades[symbol].apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)
    in_sample_long_point = in_sample_short_long_points[in_sample_short_long_points > 0]
    in_sample_short_point = in_sample_short_long_points[in_sample_short_long_points < 0]
    
    # Plot in-sample trade orders
    plt.figure()
    plot_df = pd.concat([in_sample_trade_orders, benchmark_in_sample_trade_orders], keys=["Manual Strategy", "Benchmark"], axis=1) 
    plot_df.plot(kind="line", color={"red": "Manual Strategy", "purple": "Benchmark"})

    in_sample_plot_min = in_sample_trade_orders.min()-0.25
    in_sample_plot_max = in_sample_trade_orders.max()+0.25

    plt.ylim(in_sample_plot_min, in_sample_plot_max)
    plt.vlines(x=in_sample_long_point.index, ymin=in_sample_plot_min, ymax=in_sample_plot_max, color="blue", linestyle='--', label="Long Entry")
    plt.vlines(x=in_sample_short_point.index, ymin=in_sample_plot_min, ymax=in_sample_plot_max, color="black", linestyle='--', label="Short Entry")

    plot_figure("In-Sample Manual Strategy vs Benchmark", ["Manual Strategy", "Benchmark", "Long Entry", "Short Entry"], "figure_manual_strategy_in_sample")

    # Calculate in-sample statistics
    in_sample_statistics = calculate_statistics(benchmark_in_sample_port_val, in_sample_port_val)
    in_sample_statistics.to_csv('./images/p8_results_in_sample.txt', sep='\t', index=False, header=True)

    ############################################################################################################################ 

    # Get out-of-sample data
    out_of_sample_trades = manual_strategy.testPolicy(symbol, sd=out_sample_sd, ed=out_sample_ed)

    # Create out-of-sample trade order table
    out_of_sample_trade_order_table = create_order_table(symbol, out_of_sample_trades)

    # Get normalized out-of-sample trade orders
    out_of_sample_port_val = markism.compute_portvals(out_of_sample_trade_order_table, commission=9.95, impact=0.005)
    out_of_sample_trade_orders = normalize_values(out_of_sample_port_val)

    # Get out-of-sample benchmark data
    prices_all = get_data([symbol], pd.date_range(out_sample_sd, out_sample_ed))
    prices = prices_all[[symbol]]
    
   # Create out-of-sample trade order table
    benchmark_out_of_sample_orders = create_benchmark_orders(prices)

    # Get normalized out-of-sample trade orders
    benchmark_out_of_sample_port_val = markism.compute_portvals(benchmark_out_of_sample_orders, commission=9.95, impact=0.005)
    benchmark_out_of_sample_trade_orders = normalize_values(benchmark_out_of_sample_port_val)

    # Set long/short entry points
    out_of_sample_short_long_points = out_of_sample_trades[symbol].apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)
    out_of_sample_long_point = out_of_sample_short_long_points[out_of_sample_short_long_points > 0]
    out_of_sample_short_point = out_of_sample_short_long_points[out_of_sample_short_long_points < 0]

    # Plot out-of-sample trade orders
    plt.figure()
    plot_df = pd.concat([out_of_sample_trade_orders, benchmark_out_of_sample_trade_orders], keys=["Manual Strategy", "Benchmark"], axis=1) 
    plot_df.plot(kind="line", color={"red": "Manual Strategy", "purple": "Benchmark"})  

    out_of_sample_plot_min = out_of_sample_trade_orders.min()-0.25
    out_of_sample_plot_max = out_of_sample_trade_orders.max()+0.25
    
    plt.ylim(out_of_sample_plot_min, out_of_sample_plot_max)
    plt.vlines(x=out_of_sample_long_point.index, ymin=out_of_sample_plot_min, ymax=out_of_sample_plot_max, color="blue", linestyle='--', label="Long Entry")
    plt.vlines(x=out_of_sample_short_point.index, ymin=out_of_sample_plot_min, ymax=out_of_sample_plot_max, color="black", linestyle='--', label="Short Entry")
      
    plot_figure("Out-of-Sample Manual Strategy vs Benchmark", ["Manual Strategy", "Benchmark", "Long Entry", "Short Entry"], "figure_manual_strategy_out_of_sample")

    # Calculate out-of-sample statistics
    out_of_sample_statistics = calculate_statistics(benchmark_out_of_sample_port_val, out_of_sample_port_val)
    out_of_sample_statistics.to_csv('./images/p8_results_out_of_sample.txt', sep='\t', index=False, header=True)

    ############################################################################################################################  
    
    # Run experiment one
    experiment_one = experiment1.ExperimentOne()
    
    # Get in-sample data
    manual_trade_orders, strategy_trade_orders, benchmark_trade_orders = experiment_one.run(symbol, sd=in_sample_sd, ed=in_sample_ed)

    # Plot in-sample data
    plt.figure()
    plot_df = pd.concat([manual_trade_orders, strategy_trade_orders, benchmark_trade_orders], keys=["Manual Strategy", "Strategy Learner", "Benchmark"], axis=1) 
    plot_df.plot(kind="line")        
    plot_figure("Experiment 1 - In-Sample Comparisons", ["Manual Strategy", "Strategy Learner", "Benchmark"], "figure_experiment_one_in_sample")

    # Get out-of-sample data
    manual_trade_orders, strategy_trade_orders, benchmark_trade_orders = experiment_one.run(symbol, sd=out_sample_sd, ed=out_sample_ed)

    # Plot out-of-sample data
    plt.figure()
    plot_df = pd.concat([manual_trade_orders, strategy_trade_orders, benchmark_trade_orders], keys=["Manual Strategy", "Strategy Learner", "Benchmark"], axis=1) 
    plot_df.plot(kind="line")        
    plot_figure("Experiment 1 - Out-Of-Sample Comparisons", ["Manual Strategy", "Strategy Learner", "Benchmark"], "figure_experiment_one_out_of_sample")

    ########################################################################################################################### 
    
    # Run experiment two
    experiment_two = experiment2.ExperimentTwo()
    experiment_two.run(symbol, sd=in_sample_sd, ed=in_sample_ed)
