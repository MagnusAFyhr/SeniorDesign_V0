"""

Title : account_metrics.py
Author : Magnus Fyhr
Created : 02/03/2020

Purpose :

Development :

Testing :

TO-DO:

Comments:
    - each trade should get its own trade object

"""

# should iterate through trades history and make trade dictionaries for each trade
# trade dict
#   - type :
#   - open date :
#   - close date :
#   - is_win :
#   - earnings :
#   - holding time :
#   - account net worth :

# what matters :
#
# winning/losing streaks
# per trade type (long/short)
# per trade earnings
# per trade holding times

def analyze_account_history(account_history):

    for log in account_history:
        if log["action"] == "LONG":
            pass

        pass



    trade = {
        "type": 0,
        "open_date": 0,
        "close_date": 0,
        "is_win": 0,
        "earnings": 0,
        "holding_time": 0,
        "net_worth": 0
    }

    pass

def account_statistics(account_history):
    # convert account history to trade history

    # initialize dictionary object for statistics
    trades_stats = {
        "total": 0,                         # long + short count
        "net_earnings": 0,                  # SUM( trades earnings )
        "avg_earnings": 0,                  # net worth / total trades
        "avg_holding_time": 0,              # SUM( trade holding time ) / total trades
        "max_drawdown": 0,                  #
        "long": {
            "count": 0,                     # long count
            "net_earnings": 0,              # SUM( longs revenue )
            "avg_earnings": 0,              # net earnings / long count                         ***
            "long_pct": 0,                  # long count / total trades                         ***
            "winners": {
                "count": 0,                 # winning long count
                "net_gain": 0,              # SUM( winning longs earnings )
                "win_pct": 0,               # winning long count / total long count             ***
                "avg_gain": 0,              # net long gain / long count                        ***
                "high_gain": 0,             # highest earnings from long
                "most_consec_wins": 0,      # highest winning streak
                "avg_consec_wins": 0,       # AVG( winning streaks )
                "avg_holding_time": 0       # AVG( winning holding times )
            },
            "losers": {
                "count": 0,                 # losing long count
                "net_loss": 0,              # SUM( losing longs revenue )
                "lose_pct": 0,              # losing long count / total long count
                "avg_loss": 0,              # net long loss / long count
                "high_loss": 0,             # highest loss from long
                "most_consec_losses": 0,    # highest losing streak
                "avg_consec_losses": 0,     # AVG( losing streaks )
                "avg_holding_time": 0       # AVG( losing holding times )
            }
        },
        "short": {
            "count": 0,
            "net_earnings": 0,
            "avg_earnings": 0,
            "winners": {
                "count": 0,                 # short count
                "net_gain": 0,              # SUM( winning shorts revenue )
                "win_pct": 0,               # winning short count / total short count
                "avg_gain": 0,              #
                "high_gain": 0,             #
                "most_consec_wins": 0,      #
                "avg_consec_wins": 0,       #
                "avg_holding_time": 0       #
            },
            "losers": {
                "count": 0,
                "net_loss": 0,
                "lose_pct"
                "avg_loss": 0,
                "high_loss": 0,
                "most_consec_losses": 0,
                "avg_consec_losses": 0,
                "avg_holding_time": 0
            }
        }
    }

    return trades_stats




def ratios():
    pass


def roi(start_balance, end_balance):
    """ Return On Investment """
    return end_balance / start_balance


def r_value():
    """ R-value """
    pass


def max_draw_down():
    """ Maximum Draw Down """


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
