"""

Title : calculator.py
Author : Magnus Fyhr
Created : 1/5/2020

Purpose : Calculate all technical indicators.

Development :

Testing :

"""

import data.driver.helper.indicators.overlap_studies as calc_os
import talib


def build_pure_row(index, raw_df):
    basic_indicators = calculate_basic_indicators(index, raw_df)
    pass


def calculate_basic_indicators(index, raw_df):
    RSI = talib._ta_lib.RSI()
    return list([])

def calculate_overlap_studies(index, raw_df):
    BBANDS = calc_os.BBANDS(index, raw_df)
    DEMA = calc_os.DEMA(index, raw_df)
    EMA = calc_os.EMA(index, raw_df)
    HT_TRENDLINE = calc_os.HT_TRENDLINE(index, raw_df)
    KAMA = calc_os.KAMA(index, raw_df)
    MA = calc_os.MA(index, raw_df)
    MAMA = calc_os.MAMA(index, raw_df)
    MAVP = calc_os.MAVP(index, raw_df)
    MIDPOINT = calc_os.MIDPOINT(index, raw_df)
    MIDPRICE = calc_os.MIDPRICE(index, raw_df)
    SAR = calc_os.SAR(index, raw_df)
    SAREXT = calc_os.SAREXT(index, raw_df)
    SMA = calc_os.SMA(index, raw_df)
    T3 = calc_os.T3(index, raw_df)
    TEMA = calc_os.TEMA(index, raw_df)
    WMA = calc_os.WMA(index, raw_df)

    return list([BBANDS, DEMA, EMA, HT_TRENDLINE, KAMA,
                 MA, MAMA, MAVP, MIDPOINT, MIDPRICE,
                 SAR, SAREXT, SMA, T3, TEMA, WMA])


def calculate_momentum_indicators(input_data):
    pass


def calculate_volume_indicators(input_data):
    pass


def calculate_volatility_indicators(input_data):
    pass


# there are more




