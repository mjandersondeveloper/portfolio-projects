import datetime as dt  		  	   		  		 			  		 			     			  	  	   		  		 			  		 			     			  	 
import pandas as pd
import matplotlib.pyplot as plt

import TheoreticallyOptimalStrategy as tos
import indicators as ind

from marketsimcode import compute_portvals	   		  		 			  		 			     			  	 
from util import get_data

def author():  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
    return "manderson332"

def normalize_values(df):
    return df/df.iloc[0]

def plot_figure(title, legend, save_filename, normalized_data=False):
    # Title
    plt.title(title) 

    # Labels
    plt.xlabel("Date")
    plt.ylabel("Normalized Price") if normalized_data else plt.ylabel("Price")
    plt.xticks(rotation=30) # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xticks.html

    # Legend and save
    if legend: plt.legend(legend)
    plt.savefig("./images/" + save_filename + ".png")

def fillna_data(df):
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

def plot_sma(prices, five_day_sma):
    plot_df = pd.concat([prices, five_day_sma], keys=["JPM Price", "5-day SMA"], axis=1) 
    plot_df.plot(kind="line")

    plot_figure("5-day Simple Moving Average", ["JPM Price", "5-day SMA"], "Figure_SMA")

def plot_ema(prices, ten_day_ema):
    plot_df = pd.concat([prices, ten_day_ema], keys=["JPM Prices", "10-day EMA"], axis=1) 
    plot_df.plot(kind="line")

    plot_figure("10-day Exponential Moving Average", ["JPM Prices","10-day EMA"], "Figure_EMA")

def plot_percent_b_indicator(middle, upper, lower, percent_b):
    fillna_data(middle)
    fillna_data(upper)
    fillna_data(lower)
    fillna_data(percent_b)

    # Create subplot - https://www.statology.org/pandas-subplots/
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)
    plot_df = pd.concat([upper, middle, lower], keys=["Upper Band", "Middle Band (SMA)", "Lower Band"], axis=1)  
    plot_df.plot(ax=axes[0], kind="line")
    axes[0].legend(["Upper Band", "Middle Band (SMA)", "Lower Band"])
    
    hist_plot_df = pd.concat([percent_b], keys=["%B"], axis=1) 
    hist_plot_df.plot(ax=axes[1], kind="line")
    axes[1].legend(["%B"])

    # Add upper and lower dashed lines - https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axhline.html
    axes[1].axhline(0, linestyle='--', color="green")
    axes[1].axhline(1, linestyle='--', color="red")

    plot_figure("%B Indicator", [], "Figure_PercentB")

def plot_ppo(prices, twelve_day_ema, twenty_six_day_ema, ppo_histogram):
    fillna_data(twelve_day_ema)
    fillna_data(twenty_six_day_ema)
    fillna_data(ppo_histogram)
    
    # Create subplot
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)
    plot_df = pd.concat([prices, twelve_day_ema, twenty_six_day_ema], keys=["JPM Price", "12-day EMA", "26-day EMA"], axis=1) 
    plot_df.plot(ax=axes[0], kind="line")
    axes[0].legend(["JPM Price", "12-day EMA", "26-day EMA"])
    
    hist_plot_df = pd.concat([ppo_histogram], keys=["PPO Histogram Line"], axis=1) 
    hist_plot_df.plot(ax=axes[1], kind="line")
    axes[1].legend(["PPO Histogram Line"])

    # Add zero line
    axes[1].axhline(0, linestyle='-', color="black")

    plot_figure("Percentage Price Oscillators", [], "Figure_PPO", normalized_data=True)

def plot_macd(macd_line, signal_line, macd_histogram):
    fillna_data(macd_line)
    fillna_data(signal_line)
    fillna_data(macd_histogram)
    
    # Create subplot
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)
    plot_df = pd.concat([macd_line, signal_line], keys=["MACD Line", "Signal Line"], axis=1) 
    plot_df.plot(ax=axes[0], kind="line")
    axes[0].legend(["MACD Line", "Signal Line"])

    hist_plot_df = pd.concat([macd_histogram], keys=["MACD Histogram Line"], axis=1) 
    hist_plot_df.plot(ax=axes[1], kind="line")
    axes[1].legend(["MACD Histogram Line"])

    # Add zero line
    axes[1].axhline(0, linestyle='-', color="black")

    plot_figure("Moving Average Convergence/Divergence Oscillator", [], "Figure_MACD")

def plot_indicators(jpm_prices):
    # Simple Moving Average
    sma = ind.sma_indicator(jpm_prices)
    plot_sma(jpm_prices, sma)

    # Exponential Moving Average
    ema = ind.ema_indicator(jpm_prices)
    plot_ema(jpm_prices, ema)
    
    # %B Indicator
    bb_sma, bb_upper_band, bb_lower_band, percent_b = ind.percent_b_indicator(jpm_prices)
    plot_percent_b_indicator(bb_sma, bb_upper_band, bb_lower_band, percent_b)

    # Percentage Price Oscillator
    jpm_prices_ppo = normalize_values(jpm_prices)
    ppo_short_ema, ppo_long_ema, ppo_histogram = ind.ppo_indicator(jpm_prices_ppo)
    plot_ppo(jpm_prices_ppo, ppo_short_ema, ppo_long_ema, ppo_histogram)

    # Moving Average Convergence/Divergence Oscillator
    macd_line, signal_line, macd_histogram = ind.macd_indicator(jpm_prices)
    plot_macd(macd_line, signal_line, macd_histogram)

def plot_tos_benchmark(benchmark, port_val):
    fillna_data(port_val)
    fillna_data(benchmark)
    
    plot_df = pd.concat([port_val, benchmark], keys=["TOS Portfolio", "Benchmark"], axis=1)
    plot_df.plot(kind="line", color={"red": "TOS Portfolio", "purple": "Benchmark"})
    
    plot_figure("TOS Portfolio vs. Benchmark", ["TOS Portfolio", "Benchmark"], "Figure_TOS_Benchmark")

def get_tos_data():
    # Get trades from TOS
    jpm_trades = tos.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)

    # Make order dataframe for portval caluclation
    jpm_orders = jpm_trades.copy()
    
    jpm_orders.rename(columns={"JPM": "Shares"}, inplace=True)
    jpm_orders = jpm_orders.loc[jpm_orders["Shares"] != 0]

    jpm_orders["Symbol"] = "JPM"
    jpm_orders["Order"] = jpm_orders["Shares"].apply(lambda x: "BUY" if x > 0 else "SELL")
    jpm_orders["Shares"] = jpm_orders["Shares"].abs()

    return jpm_orders

def calculate_statistics(benchmark, port_val) :
    benchmark_daily_rets = benchmark.pct_change().dropna()
    port_val_daily_rets = port_val.pct_change().dropna()

    # Benchmark statistics
    benchmark_cr = ((benchmark.iloc[-1]/benchmark.iloc[0]) - 1).round(6)
    benchmark_std = benchmark_daily_rets.std().round(6)
    benchmark_mean = benchmark_daily_rets.mean().round(6)
    
    # Portfolio statistics
    port_val_cr = ((port_val.iloc[-1]/port_val.iloc[0]) - 1).round(6)
    port_val_std = port_val_daily_rets.std().round(6)
    port_val_mean = port_val_daily_rets.mean().round(6)
    
    return pd.DataFrame(data=[["Benchmark", benchmark_cr, benchmark_std, benchmark_mean], ["TOS", port_val_cr, port_val_std, port_val_mean]], columns=["Portfolio Type", "Cumulative return", "Standard Deviation", "Mean"])

if __name__ == "__main__":  		  	   		  		 			  		 			     			  	  		  	   		  		 			  		 			     			  	 
    # Parameters
    sd=dt.datetime(2008, 1, 1)
    ed=dt.datetime(2009,12,31)
    dates = pd.date_range(sd, ed)

    symbol="JPM"
    jpm_df = get_data([symbol], dates)
    jpm_prices = jpm_df[[symbol]]
    
    # Plot indicators
    plot_indicators(jpm_prices)
    
    # Run Theoretically Optimal Strategy (TOS)
    jpm_orders = get_tos_data()
    
    # Calculate portvals and normalize
    port_val_orders = compute_portvals(jpm_orders)
    port_val = normalize_values(port_val_orders)

    # Calculate benchmark values and normalize values
    benchmark_orders = jpm_orders.copy()
    benchmark_orders["Order"] = "BUY"
    benchmark_orders["Shares"] = 0
    benchmark_orders.iloc[0, benchmark_orders["Shares"]] = 1000

    benchmark_port_val = compute_portvals(benchmark_orders)
    benchmark = normalize_values(benchmark_port_val)

    # Plot Portfolio vs Benchmark Data
    plot_tos_benchmark(benchmark, port_val)

    # Calculate and save statistics
    statistics = calculate_statistics(benchmark, port_val)
    statistics.to_csv('./images/p6_results.txt', sep='\t', index=False, header=True) # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
    
    

