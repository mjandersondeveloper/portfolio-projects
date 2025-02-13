import numpy as np  		  	   		  		 			  		 			     			  	 	   		  		 			  		 			     			  	 

def author():  		  	   		  		 			  		 			     			  	 	  	   		  		 			  		 			     			  	 
    return "manderson332"

def sma_indicator(df, days=5):
    return df.rolling(window=days).mean()
    
def ema_indicator(df, period=10):
    # Calculate EMA
    return df.ewm(span=period).mean()

def get_multiple_emas(df, periods):
    emas = []
    for period in periods:
        emas.append(ema_indicator(df, period))
    
    return emas

def percent_b_indicator(df, symbol, days=20, factor=2, return_signals=False):
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

    # Return trade signals
    if return_signals:
        percent_b_signals = np.zeros(df.shape[0])

        # Indicate buy/sell based on percentage thresholds
        percent_b_signals[percent_b[symbol] < 0.2] = 1
        percent_b_signals[percent_b[symbol] > 0.8] = -1

        return percent_b_signals
    return percent_b

def ppo_indicator(df, symbol, short_span=12, long_span=26, signal_span=9, return_signals=False):
     # Calculate the short-term/long-term EMA, and signal line
    short_ema, long_ema = get_multiple_emas(df, [short_span, long_span])

    # Calculate PPO
    ppo = ((short_ema - long_ema) / long_ema) * 100

    # Calculate the signal line and histogram
    signal_line = ema_indicator(df=ppo, period=signal_span)
    ppo_histogram = ppo - signal_line

    # Return trade signals
    if return_signals:
        ppo_signals = np.zeros(df.shape[0])

        # Indicate buy/sell based on signal line
        ppo_signals[ppo_histogram[symbol] < -0.05] = 1 
        ppo_signals[ppo_histogram[symbol] > 1.05] = -1

        return ppo_signals
    return ppo_histogram

def macd_indicator(df, symbol, short_span=12, long_span=26, signal_span=9, return_signals=False):
    # Calculate the short-term/long-term EMA
    short_ema, long_ema = get_multiple_emas(df, [short_span, long_span])

    # Calculate MACD line
    macd_line = short_ema - long_ema

    # Calculate signal line and histogram
    signal_line = ema_indicator(df=macd_line, period=signal_span)
    macd_histogram = macd_line - signal_line

    # Return trade signals
    if return_signals:
        macd_signals = np.zeros(df.shape[0])

        # Indicate buy/sell based on value from previous date
        for i in range(1, df.shape[0]):
            if macd_histogram[symbol].iloc[i] > macd_histogram[symbol].iloc[i-1]:
                macd_signals[i] = 1
            elif macd_histogram[symbol].iloc[i] < macd_histogram[symbol].iloc[i-1]:
                macd_signals[i] = -1

        return macd_signals
    return macd_histogram
