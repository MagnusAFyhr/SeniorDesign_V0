"""

Title : calculator.py
Author : Magnus Fyhr
Created : 1/5/2020

Purpose : Calculate all technical indicators.

Development :

Testing :

"""

import data.driver.helper.indicators.overlap_studies as calc_os
import data.driver.helper.indicators.momentum_indicators as calc_mom
import data.driver.helper.indicators.statistic_functions as calc_stat
import data.driver.helper.indicators.volatility_indicators as calc_vola
import data.driver.helper.indicators.volume_indicators as calc_volu

def build_pure_dataframe(raw_df):
    #basic_indicators = calculate_basic_indicators(raw_df)

    calculate_momentum_indicators(raw_df)
    calculate_overlap_studies(raw_df)
    calculate_statistic_functions(raw_df)
    calculate_volatility_indicators(raw_df)
    calculate_volume_indicators(raw_df)

    pure_df = raw_df

    return pure_df

def calculate_basic_indicators(raw_df):
    return list([])

def calculate_momentum_indicators(raw_df):

    ADX = calc_mom.ADX(raw_df)
    ADXR = calc_mom.ADXR(raw_df)
    APO = calc_mom.APO(raw_df)
    AROON = calc_mom.AROON(raw_df)
    AROONOSC = calc_mom.AROONOSC(raw_df)
    BOP = calc_mom.BOP(raw_df)
    CCI = calc_mom.CCI(raw_df)
    CMO = calc_mom.CMO(raw_df)
    DX = calc_mom.DX(raw_df)
    MACD = calc_mom.MACD(raw_df)
    MACDEXT = calc_mom.MACDEXT(raw_df)
    MACDFIX = calc_mom.MACDFIX(raw_df)
    MFI = calc_mom.MFI(raw_df)
    MINUS_DI = calc_mom.MINUS_DI(raw_df)
    MINUS_DM = calc_mom.MINUS_DM(raw_df)
    MOM = calc_mom.MOM(raw_df)
    PLUS_DI = calc_mom.PLUS_DI(raw_df)
    PLUS_DM = calc_mom.PLUS_DM(raw_df)
    PPO = calc_mom.PPO(raw_df)
    ROC = calc_mom.ROC(raw_df)
    ROCP = calc_mom.ROCP(raw_df)
    ROCR = calc_mom.ROCR(raw_df)
    ROCR100 = calc_mom.ROCR100(raw_df)
    RSI = calc_mom.RSI(raw_df)
    STOCH = calc_mom.STOCH(raw_df)
    STOCHF = calc_mom.STOCHF(raw_df)
    STOCHRSI = calc_mom.STOCHRSI(raw_df)
    TRIX = calc_mom.TRIX(raw_df)
    ULTOSC = calc_mom.ULTOSC(raw_df)
    WILLR = calc_mom.WILLR(raw_df)

    # add verification
    # if it fails; return false

    raw_df["ADX"] = ADX
    raw_df["ADXR"] = ADXR
    raw_df["APO"] = APO
    raw_df["AROON"] = AROON
    raw_df["AROONOSC"] = AROONOSC
    raw_df["BOP"] = BOP
    raw_df["CCI"] = CCI
    raw_df["CMO"] = CMO
    raw_df["DX"] = DX
    raw_df["MACD"] = MACD
    raw_df["MACDEXT"] = MACDEXT
    raw_df["MACDFIX"] = MACDFIX
    raw_df["MFI"] = MFI
    raw_df["MINUS_DI"] = MINUS_DI
    raw_df["MINUS_DM"] = MINUS_DM
    raw_df["MOM"] = MOM
    raw_df["PLUS_DI"] = PLUS_DI
    raw_df["PLUS_DM"] = PLUS_DM
    raw_df["PPO"] = PPO
    raw_df["ROC"] = ROC
    raw_df["ROCP"] = ROCP
    raw_df["ROCR"] = ROCR
    raw_df["ROCR100"] = ROCR100
    raw_df["RSI"] = RSI
    raw_df["STOCH"] = STOCH
    raw_df["STOCHF"] = STOCHF
    raw_df["STOCHRSI"] = STOCHRSI
    raw_df["TRIX"] = TRIX
    raw_df["ULTOSC"] = ULTOSC
    raw_df["WILLR"] = WILLR

    return True

def calculate_overlap_studies(raw_df):

    BBANDS = calc_os.BBANDS(raw_df)
    DEMA = calc_os.DEMA(raw_df)
    EMA = calc_os.EMA(raw_df)
    HT_TRENDLINE = calc_os.HT_TRENDLINE(raw_df)
    KAMA = calc_os.KAMA(raw_df)
    MA = calc_os.MA(raw_df)
    MAMA = calc_os.MAMA(raw_df)
    MAVP = calc_os.MAVP(raw_df)
    MIDPOINT = calc_os.MIDPOINT(raw_df)
    MIDPRICE = calc_os.MIDPRICE(raw_df)
    SAR = calc_os.SAR(raw_df)
    SAREXT = calc_os.SAREXT(raw_df)
    SMA = calc_os.SMA(raw_df)
    T3 = calc_os.T3(raw_df)
    TEMA = calc_os.TEMA(raw_df)
    WMA = calc_os.WMA(raw_df)

    # add verification
    # if it fails; return false

    raw_df["BBANDS"] = BBANDS
    raw_df["DEMA"] = DEMA
    raw_df["EMA"] = EMA
    raw_df["HT_TRENDLINE"] = HT_TRENDLINE
    raw_df["KAMA"] = KAMA
    raw_df["MA"] = MA
    raw_df["MAMA"] = MAMA
    raw_df["MAVP"] = MAVP
    raw_df["MIDPOINT"] = MIDPOINT
    raw_df["MIDPRICE"] = MIDPRICE
    raw_df["SAR"] = SAR
    raw_df["SAREXT"] = SAREXT
    raw_df["SMA"] = SMA
    raw_df["T3"] = T3
    raw_df["TEMA"] = TEMA
    raw_df["WMA"] = WMA

    # if verification passes
    # may need to return raw_df
    return True


def calculate_statistic_functions(raw_df):

    BETA = calc_stat.BETA(raw_df)
    CORREL = calc_stat.CORREL(raw_df)
    LINEARREG = calc_stat.LINEARREG(raw_df)
    LINEARREG_ANGLE = calc_stat.LINEARREG_ANGLE(raw_df)
    LINEARREG_INTERCEPT = calc_stat.LINEARREG_INTERCEPT(raw_df)
    LINEARREG_SLOPE = calc_stat.LINEARREG_SLOPE(raw_df)
    STDDEV = calc_stat.STDDEV(raw_df)
    TSF = calc_stat.TSF(raw_df)
    VAR = calc_stat.VAR(raw_df)

    raw_df["BETA"] = BETA
    raw_df["CORREL"] = CORREL
    raw_df["LINEARREG"] = LINEARREG
    raw_df["LINEARREG_ANGLE"] = LINEARREG_ANGLE
    raw_df["LINEARREG_INTERCEPT"] = LINEARREG_INTERCEPT
    raw_df["LINEARREG_SLOPE"] = LINEARREG_SLOPE
    raw_df["STDDEV"] = STDDEV
    raw_df["TSF"] = TSF
    raw_df["VAR"] = VAR

    return True



def calculate_volatility_indicators(raw_df):

    ATR = calc_vola.ATR(raw_df)
    NATR = calc_vola.NATR(raw_df)
    TRANGE = calc_vola.TRANGE(raw_df)

    raw_df["ATR"] = ATR
    raw_df["NATR"] = NATR
    raw_df["TRANGE"] = TRANGE

    return True




def calculate_volume_indicators(raw_df):

    AD = calc_volu.AD(raw_df)
    ADOSC = calc_volu.ADOSC(raw_df)
    OBV = calc_volu.OBV(raw_df)

    raw_df["AD"] = AD
    raw_df["ADOSC"] = ADOSC
    raw_df["OBV"] = OBV

    return True
