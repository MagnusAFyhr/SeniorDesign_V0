"""

Title : account_ratios.py
Author : Magnus Fyhr
Created : 02/03/2020

Purpose :

Development :

Testing :

TO-DO:

Comments:

"""


def trading_ratios(trading_history):

    ratios = {
        "profit_factor": 0,
        "gain_to_pain": 0,
        "winning_pct": 0,
        "payout_ratio": 0,
        "cpc_index": 0,
        "expectancy": 0,
        "return_pct": 0,
        "kelly_pct": 0,
        "sharpe": 0,
        "treynor": 0,
        "sortino": 0,
    }

    return ratios


def roi(start_balance, end_balance):
    """ Return On Investment """
    return end_balance / start_balance


def r_value():
    """ R-value """
    pass


def profit_factor():
    """ Profit Factor """
    pass


def winning_percentage():
    """ Winning Percentage """
    pass


def sharpe_ratio():
    """ Sharpe Ratio """
    pass


def sortino_ratio():
    """ Sortino Ratio """
    pass
