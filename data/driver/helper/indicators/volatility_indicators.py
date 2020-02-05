"""
http://mrjbq7.github.io/ta-lib/func_groups/volatility_indicators.html
"""
import talib as ta

def ATR(raw_df, timeperiod=14):
    # Average True Range
    # extract necessary data from raw dataframe (high, low, close)
    return ta.ATR(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, timeperiod)

def NATR(raw_df, timeperiod=14):
    # Normalized average true Range
    # extract necessary data from raw dataframe (high, low, close)
    return ta.NATR(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, timeperiod)

def TRANGE(raw_df):
    # True Range
    # extract necessary data from raw dataframe (high, low, close)
    return ta.TRANGE(raw_df.High.values, raw_df.Low.values, raw_df.Close.values)
