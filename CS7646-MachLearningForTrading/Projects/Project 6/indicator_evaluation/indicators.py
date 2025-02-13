import datetime as dt  		  	   		  		 			  		 			     			  	 	   		  		 			  		 			     			  	 
import pandas as pd  		  	   		  		 			  		 			     			  	 
from util import get_data

# Indicator formulas reference: https://school.stockcharts.com/doku.php?id=technical_indicators
def author():  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
    return "manderson332"

def sma_indicator(df, days=5):
    return df.rolling(window=days).mean()
    
def ema_indicator(df, period=10):
    # Calculate EMA
    return df.ewm(span=period).mean() # https://stackoverflow.com/questions/56593409/how-to-solve-attributeerror-module-pandas-has-no-attribute-ewma

def percent_b_indicator(df, days=20, factor=2):
    # Calculate SMA (Middle Band)
    middle_band = sma_indicator(df, days)

    # Calculate STD
    std = df.rolling(window=days).std()

    # Calculate the upper/lower Bollinger Bands
    std_factor = std * factor
    upper_band = middle_band + std_factor
    lower_band = middle_band - std_factor

    # Calculate %B
    percent_b = (df - lower_band) / (upper_band - lower_band)

    return middle_band, upper_band, lower_band, percent_b

def ppo_indicator(df, short_span=12, long_span=26, signal_span=9):
     # Calculate the short-term/long-term EMA, and signal line
    short_ema, long_ema = get_multiple_emas(df, [short_span, long_span])

    # Calculate PPO
    ppo = ((short_ema - long_ema) / long_ema) * 100

    # Calculate the signal line and histogram
    signal_line = ema_indicator(df=ppo, period=signal_span)
    ppo_histogram = ppo - signal_line

    return short_ema, long_ema, ppo_histogram

def macd_indicator(df, short_span=12, long_span=26, signal_span=9):
    # Calculate the short-term/long-term EMA
    short_ema, long_ema = get_multiple_emas(df, [short_span, long_span])

    # Calculate MACD line
    macd_line = short_ema - long_ema

    # Calculate signal line and histogram
    signal_line = ema_indicator(df=macd_line, period=signal_span)
    macd_histogram = macd_line - signal_line

    return macd_line, signal_line, macd_histogram

def get_multiple_emas(df, periods):
    emas = []
    for period in periods:
        emas.append(ema_indicator(df, period))
    
    return emas
