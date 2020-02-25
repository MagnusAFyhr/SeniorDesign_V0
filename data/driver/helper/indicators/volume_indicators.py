"""
http://mrjbq7.github.io/ta-lib/func_groups/volume_indicators.html
"""
import talib as ta
import numpy as np

def AD(raw_df):
    # Chaikin A/D Line
    # extract necessary data from raw dataframe (high, low, close, volume)
    return ta.ATR(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, raw_df.Volume.values)

def ADOSC(raw_df, fastperiod=3, slowperiod=10):
    # Chaikin A/D Oscillator
    # extract necessary data from raw dataframe (high, low, close, volume)
    return ta.ADOSC(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, raw_df.Volume.values.astype(float), fastperiod, slowperiod)

def OBV(raw_df):
    # On Balance Volume
    # extract necessary data from raw dataframe (close, volume)
    return ta.OBV(raw_df.Close.values, raw_df.Volume.values.astype(float))
