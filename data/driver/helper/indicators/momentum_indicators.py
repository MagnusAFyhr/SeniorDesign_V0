"""
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html

Describe this file

"""
import talib as ta
import numpy as np

#Special Functions:
#AROON 2
#MACD 3
#MACDEXT 3
#MACDFIX 3
#STOCH 2
#STOCHF 2
#STOCHRSI 2

def ADX(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low, close)
    return ta.ADX(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, timeperiod)


def ADXR(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low, close)
    return ta.ADXR(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, timeperiod)


def APO(raw_df, fastperiod=12, slowperiod=26, matype=0):
    # extract necessary data from raw dataframe (close)
    return ta.APO(raw_df.Close.values, fastperiod, slowperiod, matype)


def AROON(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low)
    # this function returns two columns of data
    aroondown, aroonup = ta.AROON(raw_df.High.values, raw_df.Low.values, timeperiod)
    singleMerged = np.stack((aroondown, aroonup), axis=-1)
    return singleMerged.tolist()


def AROONOSC(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low)
    return ta.AROONOSC(raw_df.High.values, raw_df.Low.values, timeperiod)


def BOP(raw_df):
    # extract necessary data from raw dataframe (open, high, low, close)
    return ta.BOP(raw_df.Open.values, raw_df.High.values, raw_df.Low.values, raw_df.Close.values)


def CCI(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low, close)
    return ta.CCI(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, timeperiod)


def CMO(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (close)
    return ta.CMO(raw_df.Close.values, timeperiod)


def DX(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low, close)
    return ta.DX(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, timeperiod)


def MACD(raw_df, fastperiod=12, slowperiod=26, signalperiod=9):
    # extract necessary data from raw dataframe (close)
    # returns 3 things
    macd, macdsignal, macdhist = ta.MACD(raw_df.Close.values, fastperiod, slowperiod, signalperiod)
    singleMerged = np.stack((macd, macdsignal, macdhist), axis=-1)
    return singleMerged.tolist()


def MACDEXT(raw_df, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0):
    # extract necessary data from raw dataframe (close)
    # returns 3 things
    macd, macdsignal, macdhist = ta.MACDEXT(raw_df.Close.values, fastperiod, fastmatype, slowperiod, slowmatype, signalperiod, signalmatype)
    singleMerged = np.stack((macd, macdsignal, macdhist), axis=-1)
    return singleMerged.tolist()


def MACDFIX(raw_df, signalperiod=9):
    # extract necessary data from raw dataframe (close)
    # returns 3 things
    macd, macdsignal, macdhist = ta.MACDFIX(raw_df.Close.values, signalperiod)
    singleMerged = np.stack((macd, macdsignal, macdhist), axis=-1)
    return singleMerged.tolist()


def MFI(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low, close, volume)
    return ta.MFI(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, raw_df.Volume.values.astype(float), timeperiod)


def MINUS_DI(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low, close)
    return ta.MINUS_DI(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, timeperiod)


def MINUS_DM(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low)
    return ta.MINUS_DM(raw_df.High.values, raw_df.Low.values, timeperiod)


def MOM(raw_df, timeperiod=10):
    # extract necessary data from raw dataframe (close)
    return ta.MOM(raw_df.Close.values, timeperiod)


def PLUS_DI(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low, close)
    return ta.PLUS_DI(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, timeperiod)


def PLUS_DM(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low)
    return ta.PLUS_DM(raw_df.High.values, raw_df.Low.values, timeperiod)


def PPO(raw_df, fastperiod=12, slowperiod=26, matype=0):
    # extract necessary data from raw dataframe (close)
    return ta.PPO(raw_df.Close.values, fastperiod, slowperiod, matype)


def ROC(raw_df, timeperiod=10):
    # extract necessary data from raw dataframe (close)
    return ta.ROC(raw_df.Close.values, timeperiod)


def ROCP(raw_df, timeperiod=10):
    # extract necessary data from raw dataframe (close)
    return ta.ROCP(raw_df.Close.values, timeperiod)


def ROCR(raw_df, timeperiod=10):
    # extract necessary data from raw dataframe (close)
    return ta.ROCR(raw_df.Close.values, timeperiod)


def ROCR100(raw_df, timeperiod=10):
    # extract necessary data from raw dataframe (close)
    return ta.ROCR100(raw_df.Close.values, timeperiod)


def RSI(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (close)
    return ta.RSI(raw_df.Close.values, timeperiod)


def STOCH(raw_df, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0):
    # extract necessary data from raw dataframe (high, low, close)
    # returns 2 columns
    slowk, slowd = ta.STOCH(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, fastk_period, slowk_period, slowk_matype) #, slowd_period, slowd_matype)
    singleMerged = np.stack((slowk, slowd), axis=-1)
    return singleMerged.tolist()


def STOCHF(raw_df, fastk_period=5, fastd_period=3, fastd_matype=0):
    # extract necessary data from raw dataframe (high, low, close)
    # returns 2 columns
    fastk, fastd = ta.STOCHF(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, fastk_period, fastd_period, fastd_matype)
    singleMerged = np.stack((fastk, fastd), axis=-1)
    return singleMerged.tolist()


def STOCHRSI(raw_df, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0):
    # extract necessary data from raw dataframe (close)
    # returns 2 columns
    fastk, fastd = ta.STOCHRSI(raw_df.Close.values, timeperiod, fastk_period, fastd_period, fastd_matype)
    singleMerged = np.stack((fastk, fastd), axis=-1)
    return singleMerged.tolist()


def TRIX(raw_df, timeperiod=30):
    # extract necessary data from raw dataframe (close)
    return ta.TRIX(raw_df.Close.values, timeperiod)


def ULTOSC(raw_df, timeperiod1=7, timeperiod2=14, timeperiod3=28):
    # extract necessary data from raw dataframe (high, low, close)
    return ta.ULTOSC(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, timeperiod1, timeperiod2, timeperiod3)


def WILLR(raw_df, timeperiod=14):
    # extract necessary data from raw dataframe (high, low, close)
    return ta.WILLR(raw_df.High.values, raw_df.Low.values, raw_df.Close.values, timeperiod)
