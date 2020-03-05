"""

Title : allele_react.py
Author : Magnus Fyhr
Created : 02/19/2020

Purpose : Set of functions responsible for handling reaction with the unique technical indicators that exist; allows
    Allele to more intellectually comprehend these technical indicators.

Development :


Testing :


Comments :
- Special Technical Indicators
    + Momentum
        * AROON 2
        * MACD 3
        * MACDEXT 3
        * MACDFIX 3
        * STOCH 2
        * STOCHF 2
        * STOCHRSI 2
    + Overlap Studies
        * BBANDS 3
        * MAMA 2
    + Volatility Indicators
    + Volume Indicators

"""


def __react_AROON(allele, close_price, input_data):
    # input_data = [aroon_up, aroon_down]

    # reaction
    if allele.position == 1:  # long
        if input_data[0] > allele.position:  # condition met
            return 1 + allele.power

    elif allele.position == -1:  # short
        if input_data[1] > allele.position:  # condition met
            return 1 + allele.power

    # condition not met
    return 0


def __react_MACD(allele, close_price, input_data):
    # input_data = [macd, macd_signal, macd_hist]

    # reaction
    if allele.position == 1:  # long
        if input_data[1] > input_data[0]:  # condition met
            return 1 + allele.power

    elif allele.position == -1:  # short
        if input_data[1] < input_data[0]:  # condition met
            return 1 + allele.power

    # condition not met
    return 0


def __react_STOCH(allele, close_price,input_data):
    # input_data = [k, d]

    # reaction
    if allele.position == 1:  # long
        if input_data[1] > allele.threshold and input_data[0] > allele.threshold:  # condition met
            return 1 + allele.power

    elif allele.position == -1:  # short
        if input_data[1] < allele.threshold and input_data[0] < allele.threshold:  # condition met
            return 1 + allele.power

    # condition not met
    return 0


def __react_BBANDS(allele, close_price, input_data):
    # input_data = [upper_band, middle_band, lower_band]

    # reaction
    if allele.position == 1:  # long
        if close_price < input_data[2]:  # price is under lower band; implies oversold
            return 1 + allele.power

    elif allele.position == -1:  # short
        if close_price > input_data[0]:  # price is over upper band; implies overbought
            return 1 + allele.power

    # condition not met
    return 0


def __react_MAMA(allele, close_price, input_data):
    # input_data = [mama, fama]
    # https://www.forexstrategieswork.com/mama-mt4-indicator/

    return 0


reaction_dictionary = {
    "AROON": __react_AROON,
    "MACD": __react_MACD,           # done
    "MACD_EXT": __react_MACD,       # done
    "MACD_FIX": __react_MACD,       # done
    "STOCH": __react_STOCH,         # done
    "STOCHF": __react_STOCH,        # done
    "STOCHRSI": __react_STOCH,      # done
    "BBANDS": __react_BBANDS,       # done
    "MAMA": __react_MAMA,
}


def react(allele, close_price, input_data):

    # obtain technical indicator
    tech_ind = allele.tech_ind
    # will likely need to trim technical indicator name

    # verify technical indicator
    if tech_ind not in reaction_dictionary.keys():
        return 0

    # obtain unique reaction
    reaction = reaction_dictionary[tech_ind](allele, close_price, input_data)

    # verify reaction

    return reaction
