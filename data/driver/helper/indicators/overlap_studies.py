"""
https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
"""
import talib as ta
import numpy as np


#Special Functions:
#BBANDS 3
#MAMA 2


def BBANDS(raw_df, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0):
    # extract necessary data from raw dataframe (close)
    # returns 3 things

    upperband, middleband, lowerband = ta.BBANDS(raw_df.Close.values, timeperiod, nbdevup, nbdevdn, matype)
    singleMerged = np.stack((upperband, middleband, lowerband), axis=-1)
    return singleMerged.tolist()

def DEMA(raw_df, timeperiod=30):
    # extract necessary data from raw dataframe (close)
    return ta.DEMA(raw_df.Close.values, timeperiod)


def EMA(raw_df, timeperiod=30):
    # extract necessary data from raw dataframe (close)
    return ta.EMA(raw_df.Close.values, timeperiod)


def HT_TRENDLINE(raw_df):
    # extract necessary data from raw dataframe (close)
    return ta.HT_TRENDLINE(raw_df.Close.values)


def KAMA(raw_df, timeperiod=30):
    # extract necessary data from raw dataframe (close)
    return ta.KAMA(raw_df.Close.values, timeperiod)


def MA(raw_df, timeperiod=30, matype=0):
    # extract necessary data from raw dataframe (close)
    return ta.MA(raw_df.Close.values, timeperiod, matype)


def MAMA(raw_df, fastlimit=0, slowlimit=0):
    # extract necessary data from raw dataframe (close)
    # returns 2 things
    mama, fama = ta.MAMA(raw_df.Close.values, fastlimit, slowlimit)
    singleMerged = np.stack((mama, fama), axis=-1)
    return singleMerged.tolist()


def MAVP(raw_df, minperiod=2, maxperiod=30, matype=0):
    # extract necessary data from raw dataframe (close)
    return ta.MAVP(raw_df.Close.values, raw_df.Open.values, minperiod, maxperiod, matype)


def MIDPOINT(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (close)
    return ta.MIDPOINT(raw_df.Close.values, timeperiod)


def MIDPRICE(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low)
    return ta.MIDPRICE(raw_df.High.values, raw_df.Low.values, timeperiod)


def SAR(raw_df, acceleration=0, maximum=0):
    # extract necessary data from raw dataframe (high, low)
    return ta.SAR(raw_df.High.values, raw_df.Low.values, acceleration, maximum)


def SAREXT(raw_df, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0):
    # extract necessary data from raw dataframe (high, low)
    return ta.SAREXT(raw_df.High.values, raw_df.Low.values, startvalue, offsetonreverse, accelerationinitlong, accelerationlong, accelerationmaxlong, accelerationinitshort, accelerationshort, accelerationmaxshort)


def SMA(raw_df, timeperiod=30):
    # extract necessary data from raw dataframe (close)
    return ta.SMA(raw_df.Close.values, timeperiod)


def T3(raw_df, timeperiod=5, vfactor=0):
    # extract necessary data from raw dataframe (close)
    return ta.T3(raw_df.Close.values, timeperiod, vfactor)


def TEMA(raw_df, timeperiod=30):
    # extract necessary data from raw dataframe (close)
    return ta.TEMA(raw_df.Close.values, timeperiod)


def TRIMA(raw_df, timeperiod=30):
    # extract necessary data from raw dataframe (close)
    return ta.TRIMA(raw_df.Close.values, timeperiod)


def WMA(raw_df, timeperiod=30):
    # extract necessary data from raw dataframe (close)
    return ta.WMA(raw_df.Close.values, timeperiod)
