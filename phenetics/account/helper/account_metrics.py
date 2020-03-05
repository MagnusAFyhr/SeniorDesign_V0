"""

Title : account_metrics.py
Author : Magnus Fyhr
Created : 02/03/2020

Purpose :

Development :

Testing :

TO-DO:
    - implement max drawdown
    - fix ???_consec_abc variable calculations; they are wrong right now

Comments:
    -

"""

import datetime

# should iterate through trades history and make trade dictionaries for each trade
# trade dict
#   - type :
#   - open date :
#   - close date :
#   - is_win :
#   - earnings :
#   - holding time :
#   - account net worth :


def trading_metrics(account_history):

    # convert account history to trade history
    trade_history = convert_account_history(account_history)

    # analyze trade history
    trade_count = 0
    trade_net_earnings = 0
    trade_net_holding_time = 0

    long_count = 0
    long_net_earnings = 0
    long_net_holding_time = 0
    long_win_count = 0
    long_win_net_gain = 0
    long_win_high_gain = 0
    long_win_most_consec = 0
    long_win_net_consec = 0
    long_win_net_holding_time = 0
    long_lose_count = 0
    long_lose_net_loss = 0
    long_lose_high_loss = 0
    long_lose_most_consec = 0
    long_lose_net_consec = 0
    long_lose_net_holding_time = 0

    short_count = 0
    short_net_earnings = 0
    short_net_holding_time = 0
    short_win_count = 0
    short_win_net_gain = 0
    short_win_high_gain = 0
    short_win_most_consec = 0
    short_win_net_consec = 0
    short_win_net_holding_time = 0
    short_lose_count = 0
    short_lose_net_loss = 0
    short_lose_high_loss = 0
    short_lose_most_consec = 0
    short_lose_net_consec = 0
    short_lose_net_holding_time = 0

    #
    # begin analysis algorithm
    #
    long_curr_consec = {
        "win-loss": "",
        "streak": 0
    }
    short_curr_consec = {
        "win-loss": "",
        "streak": 0
    }

    for trade in trade_history:
        trade_count += 1
        trade_net_earnings += trade["earnings"]
        trade_net_holding_time += trade["holding_time"]

        # check long or short
        if trade["type"] == "LONG":
            long_count += 1
            long_net_earnings += trade["earnings"]
            long_net_holding_time += trade["holding_time"]
            # check win or loss
            if trade["earnings"] > 0:   # winner
                long_win_count += 1
                long_win_net_gain += trade["earnings"]
                long_win_net_holding_time += trade["holding_time"]
                # high gain
                if trade["earnings"] > long_win_high_gain:
                    long_win_high_gain = trade["earnings"]
                # most consec wins
                if long_curr_consec["win-loss"] == "LOSS":
                    # check versus max consec losses and log loss to net losses
                    if long_lose_most_consec < long_curr_consec["streak"]:
                        long_lose_most_consec = long_curr_consec["streak"]
                    long_lose_net_consec += long_curr_consec["streak"]
                    long_curr_consec["streak"] = 0
                else:
                    long_curr_consec["win-loss"] = "WIN"
                    long_curr_consec["streak"] += 1

            else:                       # loser
                long_lose_count += 1
                long_lose_net_loss += trade["earnings"]
                long_lose_net_holding_time += trade["holding_time"]
                # high loss
                if trade["earnings"] > long_lose_high_loss:
                    long_lose_high_loss = trade["earnings"]
                # most consec losses
                if long_curr_consec["win-loss"] == "WIN":
                    # check versus max consec losses and log loss to net losses
                    if long_win_most_consec < long_curr_consec["streak"]:
                        long_win_most_consec = long_curr_consec["streak"]
                    long_win_net_consec += long_curr_consec["streak"]
                    long_curr_consec["streak"] = 0
                else:
                    long_curr_consec["win-loss"] = "LOSS"
                    long_curr_consec["streak"] += 1

        elif trade["type"] == "SHORT":
            short_count += 1
            short_net_earnings += trade["earnings"]
            short_net_holding_time += trade["holding_time"]
            # check win or loss
            if trade["earnings"] > 0:   # winner
                short_win_count += 1
                short_win_net_gain += trade["earnings"]
                short_win_net_holding_time += trade["holding_time"]
                # high gain
                if trade["earnings"] > short_win_high_gain:
                    short_win_high_gain = trade["earnings"]
                # most consec wins
                if short_curr_consec["win-loss"] == "LOSS":
                    # check versus max consec losses and log loss to net losses
                    if short_lose_most_consec < short_curr_consec["streak"]:
                        short_lose_most_consec = short_curr_consec["streak"]
                    short_lose_net_consec += short_curr_consec["streak"]
                    short_curr_consec["streak"] = 0
                else:
                    short_curr_consec["win-loss"] = "WIN"
                    short_curr_consec["streak"] += 1

            else:                       # loser
                short_lose_count += 1
                short_lose_net_loss += trade["earnings"]
                short_lose_net_holding_time += trade["holding_time"]
                # high loss
                if trade["earnings"] > short_lose_high_loss:
                    short_lose_high_loss = trade["earnings"]
                # most consec losses
                if short_curr_consec["win-loss"] == "WIN":
                    # check versus max consec losses and log loss to net losses
                    if short_win_most_consec < short_curr_consec["streak"]:
                        short_win_most_consec = short_curr_consec["streak"]
                    short_win_net_consec += short_curr_consec["streak"]
                    long_curr_consec["streak"] = 0
                else:
                    short_curr_consec["win-loss"] = "WIN"
                    short_curr_consec["streak"] += 1

        else:
            print("< ERR > : Account : Improve this later")
            return None

    #
    # end analysis algorithm
    #
    trade_avg_earnings = 0
    trade_avg_holding_time = 0
    if trade_count > 0:
        trade_avg_earnings = trade_net_earnings / trade_count
        trade_avg_holding_time = trade_net_holding_time / trade_count

    long_avg_earnings = 0
    long_avg_holding_time = 0
    long_pct = 0
    long_win_pct = 0
    long_win_avg_gain = 0
    long_win_avg_consec = 0
    long_win_avg_holding_time = 0
    long_lose_pct = 0
    long_lose_avg_loss = 0
    long_lose_avg_consec = 0
    long_lose_avg_holding_time = 0
    if long_count > 0:
        long_avg_earnings = long_net_earnings / long_count
        long_avg_holding_time = long_net_holding_time / long_count
        long_pct = long_count / trade_count
        if long_win_count > 0:
            long_win_pct = long_win_count / long_count
            long_win_avg_gain = long_win_net_gain / long_win_count
            long_win_avg_consec = long_win_net_consec / long_win_count
            long_win_avg_holding_time = long_win_net_holding_time / long_win_count
        if long_lose_count > 0:
            long_lose_pct = long_lose_count / long_count
            long_lose_avg_loss = long_lose_net_loss / long_lose_count
            long_lose_avg_consec = long_lose_net_consec / long_lose_count
            long_lose_avg_holding_time = long_lose_net_holding_time / long_lose_count

    short_avg_earnings = 0
    short_avg_holding_time = 0
    short_pct = 0
    short_win_pct = 0
    short_win_avg_gain = 0
    short_win_avg_consec = 0
    short_win_avg_holding_time = 0
    short_lose_pct = 0
    short_lose_avg_loss = 0
    short_lose_avg_consec = 0
    short_lose_avg_holding_time = 0
    if short_count > 0:
        short_avg_earnings = short_net_earnings / short_count
        short_avg_holding_time = short_net_holding_time / short_count
        short_pct = short_count / trade_count
        if short_win_count > 0:
            short_win_pct = short_win_count / short_count
            short_win_avg_gain = short_win_net_gain / short_win_count
            short_win_avg_consec = short_win_net_consec / short_win_count
            short_win_avg_holding_time = short_win_net_holding_time / short_win_count
        if short_lose_count > 0:
            short_lose_pct = short_lose_count / short_count
            short_lose_avg_loss = short_lose_net_loss / short_lose_count
            short_lose_avg_consec = short_lose_net_consec / short_lose_count
            short_lose_avg_holding_time = short_lose_net_holding_time / short_lose_count

    # initialize dictionary object for statistics
    trades_stats = {
        "trade_count": trade_count,                                 # long + short count
        "win_count": long_win_count + short_win_count,              # win long count + win short count
        "net_gain": long_win_net_gain + short_win_net_gain,
        "loss_count": long_win_count + short_win_count,             # lose long count + lose short count
        "net_loss": long_lose_net_loss + short_lose_net_loss,
        "net_earnings": trade_net_earnings,                         # SUM( trades earnings )
        "avg_earnings": trade_avg_earnings,                         # net earnings / total trades
        "avg_holding_time": trade_avg_holding_time,                 # SUM( trade holding time ) / total trades
        "max_drawdown": 0,                                          #
        "long": {
            "count": long_count,                                    # long count
            "net_earnings": long_net_earnings,                      # SUM( longs revenue )
            "avg_earnings": long_avg_earnings,                      # net earnings / long count
            "avg_holding_time": long_avg_holding_time,              # net holding time / long count
            "long_pct": long_pct,                                   # long count / total trades
            "winners": {
                "count": long_win_count,                            # winning long count
                "win_pct": long_win_pct,                            # winning long count / total long count
                "net_gain": long_win_net_gain,                      # SUM( winning longs earnings )
                "avg_gain": long_win_avg_gain,                      # net long gain / long count
                "high_gain": long_win_high_gain,                    # highest earnings from long
                "most_consec_wins": long_win_most_consec,           # highest winning streak
                "avg_consec_wins": long_win_avg_consec,             # AVG( winning streaks )
                "avg_holding_time": long_win_avg_holding_time       # AVG( winning holding times )
            },
            "losers": {
                "count": long_lose_count,                           # losing long count
                "lose_pct": long_lose_pct,                          # losing long count / total long count
                "net_loss": long_lose_net_loss,                     # SUM( losing longs revenue )
                "avg_loss": long_lose_avg_loss,                     # net long loss / long count
                "high_loss": long_lose_high_loss,                   # highest loss from long
                "most_consec_losses": long_lose_most_consec,        # highest losing streak
                "avg_consec_losses": long_lose_avg_consec,          # AVG( losing streaks )
                "avg_holding_time": long_lose_avg_holding_time      # AVG( losing holding times )
            }
        },
        "short": {
            "count": short_count,                                   # short count
            "net_earnings": short_net_earnings,                     # SUM( shorts revenue )
            "avg_earnings": short_avg_earnings,                     # net earnings / short count
            "avg_holding_time": short_avg_holding_time,             # net holding time / long count
            "short_pct": short_pct,                                 # short count / total trades
            "winners": {
                "count": short_win_count,                           # winning short count
                "win_pct": short_win_pct,                           # winning short count / total short count
                "net_gain": short_win_net_gain,                     # SUM( winning shorts earnings )
                "avg_gain": short_win_avg_gain,                     # net short gain / short count
                "high_gain": short_win_high_gain,                   # highest earnings from short
                "most_consec_wins": short_win_most_consec,          # highest winning streak
                "avg_consec_wins": short_win_avg_consec,            # AVG( winning streaks )
                "avg_holding_time": short_win_avg_holding_time      # AVG( winning holding times )
            },
            "losers": {
                "count": short_lose_count,                          # losing short count
                "lose_pct": short_lose_pct,                         # losing short count / total short count
                "net_loss": short_lose_net_loss,                    # SUM( losing shorts revenue )
                "avg_loss": short_lose_avg_loss,                    # net short loss / short count
                "high_loss": short_lose_high_loss,                  # highest loss from short
                "most_consec_losses": short_lose_most_consec,       # highest losing streak
                "avg_consec_losses": short_lose_avg_consec,         # AVG( losing streaks )
                "avg_holding_time": short_lose_avg_holding_time     # AVG( losing holding times )
            }
        }
    }

    # done; return trade statistics
    return trades_stats, trade_history


def convert_account_history(account_history):
    """
    Converts an account history into a trade history
        - every individual trade gets its own dictionary object that holds that trade's performance
    """

    trade_history = list([])
    temp = list([])

    for log in account_history:
        # make new trade object
        trade = {
            "type": None,
            "open_date": None,
            "close_date": None,
            "quantity": None,
            "enter_price": None,
            "exit_price": None,
            "earnings": None,
            "holding_time": None,
            "net_worth": None
        }

        # determine action
        if log["action"] == "LONG" or log["action"] == "SHORT":
            # load basic of trade then add it to temp list
            trade["type"] = log["action"]
            trade["open_date"] = log["timestamp"]
            trade["quantity"] = log["quantity"]
            trade["enter_price"] = log["price"]
            trade["net_worth"] = log["net_worth"]
            # append to temp
            temp.append(trade)
            # done

        elif log["action"] == "EXIT_LONG":
            # complete each trade in temp; add each to trade_history list
            for wip_trade in temp:
                # sanity check; trade is a long
                if wip_trade["type"] != "LONG":
                    print("< ERR > : Account : Improve this later")
                    return None
                else:
                    # load more data into the trade
                    wip_trade["close_date"] = log["timestamp"]
                    wip_trade["exit_price"] = log["price"]
                    wip_trade["earnings"] = (wip_trade["exit_price"] - wip_trade["enter_price"]) * wip_trade["quantity"]
                    d1 = datetime.datetime.strptime(wip_trade["open_date"], "%Y-%m-%d")
                    d2 = datetime.datetime.strptime(wip_trade["close_date"], "%Y-%m-%d")
                    diff = abs((d2 - d1).days)
                    wip_trade["holding_time"] = diff - (int(diff / 7) * 2)
                    wip_trade["net_worth"] += wip_trade["earnings"]
                    # append to trade history
                    trade_history.append(wip_trade)
            # clear temp list
            temp.clear()
            # done

        elif log["action"] == "EXIT_SHORT":
            # complete each trade in temp; add each to trade_history list
            for wip_trade in temp:
                # sanity check; trade is a short
                if wip_trade["type"] != "SHORT":
                    print("< ERR > : Account : Improve this later")
                    return None
                else:
                    # load more data into the trade
                    wip_trade["close_date"] = log["timestamp"]
                    wip_trade["exit_price"] = log["price"]
                    wip_trade["earnings"] = (wip_trade["enter_price"] - wip_trade["exit_price"]) * wip_trade["quantity"]
                    d1 = datetime.datetime.strptime(wip_trade["open_date"], "%Y-%m-%d")
                    d2 = datetime.datetime.strptime(wip_trade["close_date"], "%Y-%m-%d")
                    diff = abs((d2 - d1).days)
                    wip_trade["holding_time"] = diff - (int(diff / 7) * 2)
                    wip_trade["net_worth"] += wip_trade["earnings"]
                    # append to trade history
                    trade_history.append(wip_trade)
            # clear temp list
            temp.clear()
            # done

        continue

    # done! return trade history
    return trade_history
