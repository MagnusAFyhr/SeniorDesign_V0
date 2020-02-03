"""
http://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
"""
import talib as ta

def BETA(raw_df, timeperiod=5):
    # extract necessary data from raw dataframe (high, low)
    return ta.BETA(raw_df.High.values, raw_df.Low.values, timeperiod)

def CORREL(raw_df, timeperiod=30):
    # Pearson's Correlation Coefficient
    # extract necessary data from raw dataframe (high, low)
    return ta.CORREL(raw_df.High.values, raw_df.Low.values, timeperiod)

def LINEARREG(raw_df, timeperiod=14):
    # Linear Regression
    # extract necessary data from raw dataframe (close)
    return ta.LINEARREG(raw_df.Close.values, timeperiod)

def LINEARREG_ANGLE(raw_df, timeperiod=14):
    # Linear Regression Angle
    # extract necessary data from raw dataframe (close)
    return ta.LINEARREG_ANGLE(raw_df.Close.values, timeperiod)

def LINEARREG_INTERCEPT(raw_df, timeperiod=14):
    # Linear Regression Intercept
    # extract necessary data from raw dataframe (close)
    return ta.LINEARREG_INTERCEPT(raw_df.Close.values, timeperiod)

def LINEARREG_SLOPE(raw_df, timeperiod=14):
    # Linear Regression Slope
    # extract necessary data from raw dataframe (close)
    return ta.LINEARREG_SLOPE(raw_df.Close.values, timeperiod)

def STDDEV(raw_df, timeperiod=5, nbdev=1):
    # Standard Deviation
    # extract necessary data from raw dataframe (close)
    return ta.STDDEV(raw_df.Close.values, timeperiod, nbdev)

def TSF(raw_df, timeperiod=14):
    # Time Series Forecast
    # extract necessary data from raw dataframe (close)
    return ta.TSF(raw_df.Close.values, timeperiod)

def VAR(raw_df, timeperiod=5, nbdev=1):
    # Linear Regression
    # extract necessary data from raw dataframe (close)
    return ta.VAR(raw_df.Close.values, timeperiod, nbdev)
