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
    - exit_position :
    - end           :
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
    - exit_position :
    - end           :
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
    - long          :
    - short         :
    - exit_position :
    - end           :
    - log_trade     : DONE
    - history       : DONE
    - net_worth     : DONE
    - performance   :       NEEDS IMPROVEMENT; WHAT DEFINES GOOD PERFORMANCE
    - metrics       :       NEEDS IMPROVEMENT; MORE NEEDS TO BE ADDED
    - status        : DONE

TO-DO:
    - implement metrics functions in account 'metrics.py'
    - make 'balance' variable *private* (also other important variable that external classes that should not access)

    - trade_history should be calculated in real-time

    - implement streak cool down

Comments :
    - All trades are currently dictionaries; at some point they should probably be converted to JSON strings

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

    - trade volume shouldn't need to be passed to the buy/short functions

    - only elites should call metrics()


Future Improvements:
    - Winning/Losing Trade Control: when...
        - winning holding time & winning roi > n,r
        - losing holding time & losing roi > n,r

"""

from phenetics.account.helper import account_metrics as acc_metrics
from phenetics.account.helper import account_ratios as acc_ratios
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
        self.prices = list([])

        # Setup Debug Mode
        self._debug_mode = debug
        if debug in params.ACCOUNT_DEBUG:
            self._is_debug = True

        # Verify The Account
        if self._is_debug:
            if self.verify() is False:
                print("< ERR > : Account : Failed to initialize Account, verification failed!")
                return

        # Initialization Complete!
        self.initialized = True
        return

    """
    Verify The Initialization Of The Account
    """
    def verify(self):

        # Verify The Ticker
        #if self.ticker == "":
        #   return False

        return True

    """
    Attempts To Execute The Specified Action
    """
    def do(self, action, timestamp, price):
        # Update Variables
        self.last_update = timestamp
        self.last_price = price
        self.prices.append(price)

        # Determine Action
        if action == "LONG":
            # enter long position, if possible
            success = self.long(timestamp, price, self.trade_volume)
            return success

        elif action == "SHORT":
            # enter short position, if possible
            success = self.short(timestamp, price, self.trade_volume)
            return success

        elif action == "HOLD":
            # hold current position (aka : do nothing)
            return True

        elif action == "EXIT":
            # exit current position, if possible
            success = self.exit_position(timestamp, price)
            return success

        # Handle Unrecognized Action
        if self._is_debug:
            print("< ERR > : Account : Unrecognized Action For Account do() : {}.".format(action))
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
                           price * self.curr_position["quantity"])

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
            self.log_trade(timestamp, "LONG", price, volume / price, volume)

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
                           price * self.curr_position["quantity"])

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
            #   the volume to the lender; currently
            self.curr_balance -= volume
            self.curr_streak += 1
            self.curr_cool_down = params.ACCOUNT_TRADE_COOL_DOWN

            # Log Trade
            self.log_trade(timestamp, "SHORT", price, volume / price, volume)

            # Short Complete!
            return True

    """
    Exit Any Current Positions
    """
    def exit_position(self, timestamp, price):

        if self.curr_position["action"] == "":
            return False

        elif self.curr_position["action"] == "LONG":
            # Calculate Revenue
            revenue = price * self.curr_position["quantity"]

            # Update Current Balance, Reset Streak & Cool Down
            self.curr_balance += revenue
            self.curr_streak = 0
            self.curr_cool_down = 0

            # Log Trade
            self.log_trade(timestamp, "EXIT_LONG", price,
                           self.curr_position["quantity"],
                           price * self.curr_position["quantity"])

            # Remove Position; Reset Values
            self.curr_position["action"] = ""
            self.curr_position["price"] = 0
            self.curr_position["quantity"] = 0

            return True

        elif self.curr_position["action"] == "SHORT":
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
                           price * self.curr_position["quantity"])

            # Remove Position; Reset Values
            self.curr_position["action"] = ""
            self.curr_position["price"] = 0
            self.curr_position["quantity"] = 0

            return True

        else:
            # handle unexpected value
            return False

    """
    """
    def end(self):

        self.exit_position(self.last_update, self.last_price)

        return

    """
    Logs Trade To The Trade History As A JSON Object
    """
    def log_trade(self, timestamp, action, price, quantity, volume):

        # Format Trade As A Dictionary Object
        trade_dict = {
            "timestamp": timestamp,
            "action": action,
            "price": price,
            "quantity": quantity,
            "volume": volume,
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
        return acc_ratios.roi(params.ACCOUNT_INIT_BALANCE, self.net_worth())

    """
    Returns Several Metrics Of The Accounts Behavior & Performance As A Dictionary Object
        - Obtained From 'account_metrics.py'
    """
    def metrics(self):

        # Calculate General Trading Metrics; Also Obtain Trading History
        general_metrics, trade_history = acc_metrics.trading_metrics(self.account_history)

        # Calculate Technical Metrics; Ratios, etc.
        technical_metrics = acc_ratios.trading_ratios(trade_history)

        # Format Metrics Into Dictionary Object
        summary = {
            "trading_days": len(self.prices),
            "fitness": self.performance(),
            "general": general_metrics,
            "technical": technical_metrics,
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
            "debug_mode": self._debug_mode,
            "is_debug": self._is_debug,

            "asset": self.ticker,
            "trade_volume": self.trade_volume,

            "start_balance": params.ACCOUNT_INIT_BALANCE,
            "curr_balance": self.curr_balance,
            "end_balance": self.net_worth(),

            "performance": self.performance(),
        }

        # Return Dictionary Object
        return state
