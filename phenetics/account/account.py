"""

Title : account.py
Author : Magnus Fyhr
Created : 11/24/2019

Purpose : The Account class object, responsible for providing proper
            functions and expected functionality for trading any
            given stock.

Development :
    - init          : DONE
    - verify        : DONE
    - do            : DONE
    - long          : DONE
    - short         : DONE
    - log_trade     : DONE
    - history       : DONE
    - net_worth     : DONE
    - performance   : DONE
    - metrics       :
    - status        : DONE

Testing :
    - init          : DONE
    - verify        : DONE
    - do            : DONE
    - long          : DONE
    - short         : DONE
    - log_trade     : DONE
    - history       : DONE
    - net_worth     : DONE
    - performance   : DONE
    - metrics       :
    - status        : DONE

Cleaning :
    - init          : DONE
    - verify        :       NEEDS IMPROVEMENT; CURRENTLY USELESS
    - do            : DONE
    - long          :       NEEDS THOROUGH ACCOUNTING CHECK
    - short         :       NEEDS THOROUGH ACCOUNTING CHECK
    - log_trade     : DONE
    - history       : DONE
    - net_worth     : DONE
    - performance   :       NEEDS IMPROVEMENT; WHAT DEFINES GOOD PERFORMANCE
    - metrics       :       NEEDS IMPROVEMENT; MORE NEEDS TO BE ADDED
    - status        : DONE

TO-DO:
    - implement metrics functions in account 'metrics.py'
    - make 'balance' variable *private* (also other important variable that external classes that should not access)

Comments :
    - All trades are currently dictionaries; at some point they should probably be converted to JSON strings
    -

    - Should this class log it's state after every buy/sell; in order to track performance? would be costly

    - how should Account performance be rewarded?
        + being more aggressive (aka: more trades)
        + great ROI
        + low risk, but decent ROI (aka: sharpe, sortino, etc. ratios)
        + ratio of winning:losing trades
        # ratio of $winners:$losers

    - can the verify() method be improved; useless right now
        + need someway to verify the ticker that is passed to this class

    - what other metrics are important for measuring an investors performance
        + need to figure out what's the best way to implement all these metrics

    - why should the account be limited to how much it can trade?
        - risk
        - but then bad and good behavior would distinguish more

    - SHOULD WE GET RID OF HOLD? AND MAKE IT END POSITION???

    - trade volume shouldn't need to be passed to the buy/short functions

"""
import phenetics.account.account_metrics as acc_metrics
import analysis.parameters as params


class Account(object):

    """
    Initialize & Verify The Account
    """
    def __init__(self, ticker, debug=0):

        # Pre-Initialization
        self.initialized = False
        self._debug_mode = 0
        self._is_debug = False

        self.ticker = ticker
        self.account_history = list([])
        self.curr_balance = params.ACCOUNT_INIT_BALANCE
        self.trade_volume = params.ACCOUNT_TRADE_VOLUME

        self.curr_position = {  # Make Default Current Position As A Dictionary Object
            "action": "",
            "price": 0,
            "quantity": 0,
        }

        self.curr_streak = 0
        self.curr_cool_down = 0

        self.last_update = None
        self.last_price = None

        # Setup Debug Mode
        self._debug_mode = debug
        if debug in params.ACCOUNT_DEBUG:
            self._is_debug = True

        # Verify The Account
        if self._is_debug:
            if self.verify() is False:
                print("< ERR > : Failed to initialize Account, verification failed!")
                return

        # Initialization Complete!
        self.initialized = True
        return

    """
    Verify The Initialization Of The Account
    """
    def verify(self):

        # Verify The Ticker
        if self.ticker == "":
            return False

        return True

    """
    Attempts To Execute The Specified Action
    """
    def do(self, action, timestamp, price):
        # Update Variables
        self.last_update = timestamp
        self.last_price = price

        # Determine Action
        if action == "BUY":
            # enter long position, if possible
            success = self.long(timestamp, price, self.trade_volume)
            return success

        elif action == "SELL":
            # enter short position, if possible
            success = self.short(timestamp, price, self.trade_volume)
            return success

        elif action == "HOLD":
            # hold current position (aka : do nothing)
            return True

        # Handle Unrecognized Action
        if self._is_debug:
            print("< ERR > : Unrecognized Action For Account do() : {}.".format(action))
        return None

    """
    Attempt To Enter A Long Position
    """
    def long(self, timestamp, price, volume):
        # Simulates a long position

        # If need to exit short position; calculate, update, log and remove it
        if self.curr_position["action"] == "SHORT":
            # Calculate Revenue
            revenue = self.curr_position["price"] * self.curr_position["quantity"]
            revenue += (self.curr_position["price"] - price) * self.curr_position["quantity"]

            # Update Current Balance, Reset Streak & Cool Down
            self.curr_balance += revenue
            self.curr_streak = 0
            self.curr_cool_down = 0

            # Log Trade
            self.log_trade(timestamp, "EXIT_SHORT", price,
                           self.curr_position["quantity"],
                           price * self.curr_position["quantity"],
                           revenue)

            # Remove Position
            self.curr_position["action"] = ""
            self.curr_position["price"] = 0
            self.curr_position["quantity"] = 0

        # Determine if account can buy 'volume' of asset at 'price'
        if self.curr_streak >= params.ACCOUNT_MAX_STREAK:
            # Do not allow account to long if it has reached the maximum consecutive trades
            return False

        elif self.curr_cool_down > 0:
            # Do not allow account to long if cool down active
            self.curr_cool_down -= 1
            return False

        elif self.curr_balance < volume:
            # Do not allow account to long if insufficient balance
            return False

        else:
            # If able to enter long position; set, update, and log it

            # Set Position
            if self.curr_position["action"] == "":
                # No current position; take long
                self.curr_position["action"] = "LONG"
                self.curr_position["price"] = price
                self.curr_position["quantity"] = volume / price

            elif self.curr_position["action"] == "LONG":
                # Current position is long; sum with current long
                sum_volume = (self.curr_position["price"] * self.curr_position["quantity"]) + volume
                sum_quantity = self.curr_position["quantity"] + (volume / price)
                avg_price = sum_volume / sum_quantity

                self.curr_position["price"] = avg_price
                self.curr_position["quantity"] = sum_quantity

            # Update Current Balance, Streak & Cool Down
            self.curr_balance -= volume
            self.curr_streak += 1
            self.curr_cool_down = params.ACCOUNT_TRADE_COOL_DOWN

            # Log Trade
            self.log_trade(timestamp, "LONG", price, volume / price, volume, -volume)

            # Long Complete!
            return True

    """
    Attempt To Enter A Short Position
    """
    def short(self, timestamp, price, volume):
        # Simulates a short position

        # If any current long positions; calculate, update, log and remove them
        if self.curr_position["action"] == "LONG":
            # Calculate Revenue
            revenue = price * self.curr_position["quantity"]

            # Update Current Balance, Reset Streak & Cool Down
            self.curr_balance += revenue
            self.curr_streak = 0
            self.curr_cool_down = 0

            # Log Trade
            self.log_trade(timestamp, "EXIT_LONG", price,
                           self.curr_position["quantity"],
                           price * self.curr_position["quantity"],
                           revenue)

            # Remove Position
            self.curr_position["action"] = ""
            self.curr_position["price"] = 0
            self.curr_position["quantity"] = 0

        # Determine if account can short 'volume' of asset at 'price'
        if self.curr_streak >= params.ACCOUNT_MAX_STREAK:
            # Do not allow account to short if it has reached the maximum consecutive trades
            return False

        if self.curr_cool_down > 0:
            # Do not allow account to short if cool down active
            self.curr_cool_down -= 1
            return False

        elif self.curr_balance < volume:
            # Do not allow account to short if insufficient balance
            return False

        else:
            # If able to enter short position; calculate, update, log and append it
            if self.curr_position["action"] == "":
                # No current position; take long
                self.curr_position["action"] = "SHORT"
                self.curr_position["price"] = price
                self.curr_position["quantity"] = volume / price

            elif self.curr_position["action"] == "SHORT":
                # Current position is short; sum with current short
                sum_volume = (self.curr_position["price"] * self.curr_position["quantity"]) + volume
                sum_quantity = self.curr_position["quantity"] + (volume / price)
                avg_price = sum_volume / sum_quantity

                self.curr_position["price"] = avg_price
                self.curr_position["quantity"] = sum_quantity

            # Update Current Balance, Streak & Cool Down
            #   - a short is technically borrowing, but
            #   volume will be deducted since the bot owes
            #   the volume to the lender
            self.curr_balance -= volume
            self.curr_streak += 1
            self.curr_cool_down = params.ACCOUNT_TRADE_COOL_DOWN

            # Log Trade
            self.log_trade(timestamp, "SHORT", price, volume / price, volume, -volume)

            # Short Complete!
            return True

    """
    Logs Trade To The Trade History As A JSON Object
    """
    def log_trade(self, timestamp, action, price, quantity, volume, revenue):

        # Format Trade As A Dictionary Object
        trade_dict = {
            "timestamp": timestamp,
            "action": action,
            "price": price,
            "quantity": quantity,
            "volume": volume,
            "revenue": revenue,
            "net_worth": self.net_worth()
        }

        # Append 'trade_dict' To 'trade_history'
        self.account_history.append(trade_dict)

        # Logging Complete!
        return

    """
    Returns A Log (list of dictionary objects) Of The Activity On This Account
    """
    def history(self):
        return self.account_history

    """
    Calculates The Net Value Of The Current Balance & Any Current Position
    """
    def net_worth(self):
        # Create Temp Variable For Arithmetic
        curr_net_worth = 0

        # Add Current Balance To Net Worth
        curr_net_worth += self.curr_balance

        # Check For A Current Position
        if self.curr_position["action"] == "":
            # no current position to calculate
            pass

        elif self.curr_position["action"] == "LONG":
            # calculate current value of long position
            curr_net_worth += self.last_price * self.curr_position["quantity"]

        elif self.curr_position["action"] == "SHORT":
            # calculate current value of short position
            value = self.curr_position["price"] * self.curr_position["quantity"]
            value += (self.curr_position["price"] * self.curr_position["quantity"]) - \
                     (self.last_price * self.curr_position["quantity"])
            curr_net_worth += value
            
        # Return Account's Current Net Worth
        return curr_net_worth

    """
    Return The Account's Available Balance
    """
    def balance(self):
        return self.curr_balance

    """
    Used By Individual To Measure Account Fitness
    """
    def performance(self):
        return acc_metrics.roi(params.ACCOUNT_INIT_BALANCE, self.net_worth())

    """
    Returns Several Metrics Of The Accounts Behavior & Performance As A Dictionary Object
        - Obtained From 'account_metrics.py'
    """
    def metrics(self):
        # Format Metrics Into Dictionary Object
        summary = {
            "trading_days": 0,
            "trades": acc_metrics.account_statistics(self.account_history),
            "ratios": {
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
            },
            "r_squared": 0
        }

        # Return Dictionary Object
        return summary

    """
    Returns Dictionary Representation Of Accounts's Current State
    """
    def status(self):
        # Format Account Into Dictionary Object
        state = {
            "init": self.initialized,
            "asset": self.ticker,
            "trade_volume": self.trade_volume,
            "start_balance": params.ACCOUNT_INIT_BALANCE,
            "end_balance": self.net_worth(),
            "trade_history": self.history(),
            "performance": self.performance(),
            "metrics": self.metrics(),
        }

        # Return Dictionary Object
        return state
