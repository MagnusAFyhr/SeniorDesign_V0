"""

Title : account_test.py
Author : Magnus Fyhr
Created : 12/1/2019

Purpose : To verify the functionality and consistency of the Account class.

Development :
    - test_account      : DONE
    - test_init         : DONE
    - test_do           : DONE      ( includes testing of long(), short(), balance )
    - test_logging      : DONE      ( includes testing of log_trade(), and trade_history )
    - test_accounting   : DONE      ( includes testing of net_worth(), and balance )

Testing :
    - test_account      : DONE
    - test_init         : DONE
    - test_do           : DONE
    - test_logging      : DONE
    - test_accounting   : DONE

This class will definitely need to be cleaned, commented and improved
    - test_do
    - test_logging
        + logs are in order
        + sequence of actions is valid
    - test_accounting
        + if revenue from entering and exiting positions is calculated properly
        + if balance is updated properly when entering or exiting a position

"""

import phenetics.account.account as acco
import time
import random


def test_account():

    test_difficulty = 10000

    print()
    print("< TEST > : Testing Account : Difficulty = {}.".format(test_difficulty))
    print()

    # Test Initialization
    init_test = test_init(test_difficulty)

    # Test Do
    do_test = test_do(test_difficulty)

    # Test Logging
    logging_test = test_logging(test_difficulty)

    # Test Accounting
    accounting_test = test_accounting(test_difficulty)

    print()
    print("< TEST > : Done.")
    print()

    # Return Boolean Test Result
    test_result = init_test and do_test and logging_test and accounting_test
    return test_result


def test_init(difficulty):
    sum_time = 0

    # Test initialization
    init_test = True
    # account = None
    for i in range(difficulty):
        # Execute Initialization, Log Runtime
        start_t = time.time_ns()
        account = acco.Account("TEST")
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Initialization
        if not account.initialized:
            init_test = False
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if init_test:
        print("< PASS > : Account Initialization : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Account Initialization.")

    # Return Boolean Test Result
    return init_test


def test_do(difficulty):
    sum_time = 0

    # Create Number Of Trades To Be Executed Per Sample (Iterations = difficulty * trade_count)
    trade_count = 20

    # Make Dummy Data
    timestamp = "TIMESTAMP"
    trade_types = ["BUY", "SELL", "HOLD"]

    # Test Do
    do_test = True
    fail_type = ""
    fail_data = None
    for i in range(difficulty):
        # Initialize Test Account
        account = acco.Account("TEST")

        # Make Random Trade List
        trade_list = list([])
        for _ in range(trade_count):
            trade_list.append(random.choice(trade_types))

        # Test Balance Control
        for trade in trade_list:
            # Generate A Random Price
            rand_price = random.uniform(1, 2)

            # Execute Trade, Log Runtime
            start_t = time.time_ns()
            account.do(trade, timestamp, rand_price)
            end_t = time.time_ns()
            elapsed = end_t - start_t
            sum_time += elapsed

            # Check Balance
            if account.balance() < 0:
                do_test = False
                fail_type = "NEG_BALANCE"
                fail_data = account.history()
                break
        if not do_test:
            break

    # Calculate Average Runtime
    per = sum_time / (difficulty * trade_count)

    # Print Test Result
    if do_test:
        print("< PASS > : Account Do : Average {} ns per do().".format(per))
    else:
        print("< FAIL > : Account Do : {}.".format(fail_type))
        print("<      > : Trade History : {} Trades.".format(len(fail_data)))
        for trade in fail_data:
            print("<      > : {}.".format(trade))

    # Return Boolean Test Result
    return do_test


def test_logging(difficulty):

    # Create Sample Size Based On Difficulty & Trade Count Per Sample
    trade_count = 20

    # Make Dummy Data
    trade_types = ["BUY", "SELL", "HOLD"]

    # Test Trade History
    logging_test = True
    fail_type = ""
    fail_data = None
    for i in range(difficulty):
        # Initialize Test Account
        account = acco.Account("TEST")

        # Make Random Trade List Data
        trade_list = list([])
        timestamp = 0
        for _ in range(trade_count):
            # Generate a random data
            trade_price = random.uniform(1, 2)
            trade_action = random.choice(trade_types)
            trade_json = {
                "timestamp": timestamp,
                "action": trade_action,
                "price": trade_price,
                "quantity": account.def_volume / trade_price,
                "volume": account.def_volume,
            }
            trade_list.append(trade_json)
            timestamp += 1

        # Simulate Trade List
        # log balance blocks for later use
        balance_blocks = 0
        for trade in trade_list:
            # Execute Trade
            success = account.do(trade["action"], trade["timestamp"], trade["price"])
            if not success:
                balance_blocks += 1

        # Crosscheck 'trade_list' With 'trade_history'
        trade_history = account.trade_history

        # get real lengths of 'trade_list' and 'trade_history'
        simple_trade_list = list([])
        for trade in trade_list:
            if trade["action"] == "BUY" or trade["action"] == "SELL":
                simple_trade_list.append(trade)
        simple_trade_hist = list([])
        for trade in trade_history:
            if trade["action"] == "LONG" or trade["action"] == "SHORT":
                simple_trade_hist.append(trade)

        # compare simplified trade list and history
        perf_matches = 0
        last_index = 0
        for l in range(len(simple_trade_list)):
            for h in range(last_index, len(simple_trade_hist)):
                # Check for matching timestamp
                if simple_trade_list[l]["timestamp"] == simple_trade_hist[h]["timestamp"]:
                    # Check for matching action
                    if (simple_trade_list[l]["action"] == "BUY" and simple_trade_hist[h]["action"] == "LONG") or\
                            (simple_trade_list[l]["action"] == "SELL" and simple_trade_hist[h]["action"] == "SHORT"):
                        # Check for matching price & quantity
                        if (simple_trade_list[l]["price"] == simple_trade_hist[h]["price"]) and\
                                (simple_trade_list[l]["quantity"] == simple_trade_hist[h]["quantity"]):
                            # Perfect match
                            perf_matches += 1
                            last_index = h
                        else:
                            logging_test = False
                            fail_type = "PRICE_QUANTITY_MISMATCH"
                            fail_data = [simple_trade_list, simple_trade_hist]
                            break
                    else:
                        logging_test = False
                        fail_type = "ACTION_MISMATCH"
                        fail_data = [simple_trade_list, simple_trade_hist]
                        break
            # if failure occurred, break again
            if not logging_test:
                break

        # perfect matches should match length of simple trade list; account for balance block
        if perf_matches + balance_blocks != len(simple_trade_list) and logging_test:
            logging_test = False
            fail_type = "MISSING_TRADE"
            fail_data = [simple_trade_list, simple_trade_hist]
            break

        # if failure has not already occurred; continue to next sub-test
        if logging_test:
            # check that between every shift from short/long that there is a logged exit of position
            last_trade = trade_history[0]
            for trade_index in range(1, len(trade_history)):
                this_trade = trade_history[trade_index]
                if this_trade["action"] != last_trade["action"]:
                    # if they don't match check logic
                    if last_trade["action"] == "EXIT_LONG":
                        if this_trade["action"] != "SHORT":
                            logging_test = False

                    elif last_trade["action"] == "EXIT_SHORT":
                        if this_trade["action"] != "LONG":
                            logging_test = False

                    elif last_trade["action"] == "LONG":
                        if this_trade["action"] != "EXIT_LONG":
                            logging_test = False

                    elif last_trade["action"] == "SHORT":
                        if this_trade["action"] != "EXIT_SHORT":
                            logging_test = False

                # do iteration updates
                last_trade = this_trade

                # check if failure occurred
                if not logging_test:
                    fail_type = "INVALID_TRADE_SEQ"
                    fail_data = trade_history
                    break
        else:
            break

    # Print Test Result
    if logging_test:
        print("< PASS > : Account Log Trade & Trade History.")

    else:
        print("< FAIL > : Account Log Trade & Trade History : {}.".format(fail_type))
        if fail_type == "INVALID_TRADE_SEQ":
            print("<      > : Trade History : {} Trades.".format(len(fail_data)))
            for trade in fail_data:
                print("<      > : {}.".format(trade))
        else:
            print("<      > : Expected History : {} Trades.".format(len(fail_data[0])))
            for trade in fail_data[0]:
                print("<      > : {}.".format(trade))
            print("<      > : Actual History : {} Trades.".format(len(fail_data[1])))
            for trade in fail_data[1]:
                print("<      > : {}.".format(trade))

    # Return Boolean Test Result
    return logging_test


def test_accounting(difficulty):

    # Create Sample Size Based On Difficulty & Trade Count Per Sample
    trade_count = 20

    # Make Dummy Data
    trade_types = ["BUY", "SELL", "HOLD"]

    # Test Trade History
    accounting_test = True
    fail_type = ""
    fail_data = None
    for i in range(difficulty):
        # Initialize Test Account
        account = acco.Account("TEST")

        # Make Random Trade List Data
        trade_list = list([])
        timestamp = 0
        for _ in range(trade_count):
            # Generate a random data
            trade_price = random.uniform(1, 2)
            trade_action = random.choice(trade_types)
            trade_json = {
                "timestamp": timestamp,
                "action": trade_action,
                "price": trade_price,
                "quantity": account.def_volume / trade_price,
                "volume": account.def_volume,
            }
            trade_list.append(trade_json)
            timestamp += 1

        # Simulate Trade List; Log Balances To Test Accounting
        balance_history = list([])
        for trade in trade_list:
            old_balance = account.balance()
        
            # Execute Trade
            account.do(trade["action"], trade["timestamp"], trade["price"])
            
            new_balance = account.balance()
            
            # Log Balances To Balance List
            balance_history.append([trade["timestamp"], old_balance, new_balance])

            # check negative balance
            if new_balance < 0:
                accounting_test = False
                fail_type = "NEG_BALANCE"
                fail_data = [account.trade_history, balance_history]
                break

        # Check that test has not already failed
        if not accounting_test:
            break

        # Crosscheck balance changes with logged trade history
        trade_history = account.history()
        last_trade_index = 0
        active_shorts = list([])
        for b in range(len(balance_history)):
            trades = list([])

            # Obtain all events that occurred at the same time
            curr_trade_index = last_trade_index
            curr_timestamp = balance_history[b][0]
            for t in range(curr_trade_index, len(trade_history)):
                if trade_history[t]["timestamp"] == curr_timestamp:
                    trades.append(trade_history[t])
                    last_trade_index += 1
                else:
                    break

            # if no trades for this timestamp, skip to next iteration
            if len(trades) == 0:
                continue

            # Verify the trades updated the balance properly
            balance = balance_history[b][1]
            for trade in trades:
                # if entering a position; should deduct trade volume from balance
                if trade["action"] == "LONG":
                    balance -= trade["volume"]
                elif trade["action"] == "SHORT":
                    balance -= trade["volume"]
                    active_shorts.append(trade)

                # if exiting a position; should increment balance by trade volume
                elif trade["action"] == "EXIT_LONG":
                    balance += trade["volume"]
                elif trade["action"] == "EXIT_SHORT":
                    sum_quantity = 0
                    sum_volume = 0
                    for active_short in active_shorts:
                        sum_quantity += active_short["quantity"]
                        sum_volume += active_short["volume"]
                    avg_price = sum_volume / sum_quantity
                    balance += (avg_price * trade["quantity"])
                    balance += (avg_price * trade["quantity"]) - (trade["price"] * trade["quantity"])
                    active_shorts.clear()

            # check if accounting ending balance matches derived ending balance
            upperbound = balance_history[b][2] + 0.0001 * balance_history[b][2]
            lowerbound = balance_history[b][2] - 0.0001 * balance_history[b][2]
            if balance < lowerbound or balance > upperbound:
                accounting_test = False
                fail_type = "BALANCE_MISMATCH"
                fail_data = [account.trade_history, balance_history, b, balance]
                break

            # Check that test has not already failed
            if not accounting_test:
                break

        # Check that test has not already failed
        if not accounting_test:
            break

    # Print Test Result
    if accounting_test:
        print("< PASS > : Account Trade Revenue & Balance Accounting.")
    else:
        print("< FAIL > : Account Trade Revenue & Balance Accounting : {}.".format(fail_type))
        if fail_type == "BALANCE_MISMATCH":
            print("<      > : [{}]{}.".format(fail_data[2], fail_data[3]))
        print("<      > : Trade History : {} Trades.".format(len(fail_data[0])))
        for trade in fail_data[0]:
            print("<      > : {}.".format(trade))
        print("<      > : Balance History : {} Trades.".format(len(fail_data[1])))
        for balance in fail_data[1]:
            print("<      > : {}.".format(balance))

    # Return Boolean Test Result
    return accounting_test
