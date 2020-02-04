"""

Title : account.py
Author : Magnus Fyhr
Created : 11/24/2019

Purpose : The Account class object, responsible for providing proper
            functions and expected functionality for trading any
            given stock.

Development :
    - init          : DONE
    - verify        : DONE (Add function from data manager, to check if ticker is supported)
    - do            : DONE
    - long          : DONE
    - short         : DONE
    - log_trade     : DONE
    - history       : DONE
    - balance       : DONE
    - net_worth     : DONE
    - performance   : DONE
    - metrics       :
    - status        : DONE

Testing :
    - init          : DONE
    - verify        : DONE (Add function from data manager, to check if ticker is supported)
    - do            : DONE
    - long          : DONE
    - short         : DONE
    - log_trade     : DONE
    - history       : DONE
    - balance       : DONE
    - net_worth     : DONE
    - performance   : DONE
    - metrics       :
    - status        : DONE

TO-DO:
    - Account performance should be rewarded for being more aggressive
    - Need to add streak along with cool down
    - Add function for sharpe ratio
    - Behavior should be able to be controlled from high-level class
    - Implement a statistics function that returns a json object (actually dict, but oh well)
    - what other metrics are important for measuring an investors performance

"""

import analysis.parameters as params


class Account(object):

    initialized = False
    _debug_mode = False

    ticker = ""
    trade_history = list([])
    curr_balance = params.ACCOUNT_DEFAULT_BALANCE
    trade_volume = params.ACCOUNT_DEFAULT_VOLUME

    # Make Default Current Position As A JSON Object
    curr_position = {
            "action": "",
            "price": 0,
            "quantity": 0,
        }

    curr_streak = 0
    curr_cool_down = 0

    last_update = None
    last_price = None

    """
    Initialize & Verify The Account
    """
    def __init__(self, ticker, debug=False):

        # Initialize The Account
        self._debug_mode = debug
        self.ticker = ticker

        # Verify The Account
        if self.verify() is False:
            print("< ERR > : Failed to initialize Account, verification failed!")
            return

        # Done Initializing
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
        if action is None:
            print("< ERR > : NoneType Action Received For Account do().")
            return None

        elif action == "BUY":
            # Enter long position, if possible
            success = self.long(timestamp, price, self.trade_volume)
            return success

        elif action == "SELL":
            # Enter short position, if possible
            success = self.short(timestamp, price, self.trade_volume)
            return success

        elif action == "HOLD":
            # Hold current position (aka : do nothing)
            return True

        # Handle Unrecognized Action
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
            revenue += (self.curr_position["price"] * self.curr_position["quantity"]) -\
                       (price * self.curr_position["quantity"])

            # Update Current Balance & Streak
            self.curr_balance += revenue
            self.curr_streak = 0

            # Log Trade
            self.log_trade(timestamp, "EXIT_SHORT", price, self.curr_position["quantity"],
                           price * self.curr_position["quantity"])

            # Remove Position
            self.curr_position["action"] = ""
            self.curr_position["price"] = 0
            self.curr_position["quantity"] = 0

        # Determine if account can buy 'volume' of asset at 'price'
        if self.curr_cool_down > 0:
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
            # self.curr_cool_down = self.def_trade_cool_down

            # Log Trade
            self.log_trade(timestamp, "LONG", price, volume / price, volume)

            # Done
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

            # Update Current Balance & Streak
            self.curr_balance += revenue
            self.curr_streak = 0

            # Log Trade
            self.log_trade(timestamp, "EXIT_LONG", price, self.curr_position["quantity"],
                           price * self.curr_position["quantity"])

            # Remove Position
            self.curr_position["action"] = ""
            self.curr_position["price"] = 0
            self.curr_position["quantity"] = 0

        # Determine if account can buy 'volume' of asset at 'price'
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
            # a short is technically borrowing, but volume will be deducted since the bot owes the volume to the lender
            self.curr_balance -= volume
            self.curr_streak += 1
            # self.curr_cool_down = self.def_trade_cool_down

            # Log the trade
            self.log_trade(timestamp, "SHORT", price, volume / price, volume)

            # Done
            return True

    """
    Logs Trade To The Trade History As A JSON Object
    """
    def log_trade(self, timestamp, action, price, quantity, volume):

        # Format trade as a JSON object
        trade_json = {
            "timestamp": timestamp,
            "action": action,
            "price": price,
            "quantity": quantity,
            "volume": volume,
        }

        # Append 'trade_json' to 'trade_history'
        self.trade_history.append(trade_json)

        # Done
        return

    """
    Returns A Log (list) Of The Activity Of This Account
    """
    def history(self):
        return self.trade_history

    """
    Returns The Current Available Capital To Invest
    """
    def balance(self):
        return self.curr_balance

    """
    Calculates The Net Value Of The Current Balance & Any Current Positions
    """
    def net_worth(self):
        curr_net_worth = 0

        # Add current balance to net worth
        curr_net_worth += self.curr_balance

        # Is their a current position?
        if self.curr_position["action"] == "":
            # No current position to calculate
            curr_net_worth += 0

        elif self.curr_position["action"] == "LONG":
            # Calculate current value of long position
            revenue = self.last_price * self.curr_position["quantity"]
            curr_net_worth += revenue

        elif self.curr_position["action"] == "SHORT":
            # Calculate current value of long position
            revenue = self.last_price * self.curr_position["quantity"]
            curr_net_worth += revenue

        # Return Account's Current Net Worth
        return curr_net_worth

    """
    Calculates The ROI Of The Account
    """
    def roi(self):
        # Calculate ROI based on accounts net worth and starting balance
        roi = self.net_worth() / params.ACCOUNT_DEFAULT_BALANCE

        # Return the ROI
        return roi

    """
    Used By Individual To Measure Account Fitness
    """
    def performance(self):
        return self.roi()

    """
    Returns Several Metrics Of The Accounts Behavior & Performance As A JSON Object; Obtained From 'account_metrics.py'
    """
    def metrics(self):

        # Format Metrics Into JSON Object
        json = {
            "roi": self.roi(),
            "sharpe_ratio": self.sharpe_ratio(),
        }

        # Return JSON Object
        return json

    """
    Returns JSON Representation Of The Account Class
    """
    def status(self):

        # Format Account Class Into JSON Object
        json = {
            "init": self.initialized,
            "asset": self.ticker,
            "trade_volume": self.trade_volume,
            "start_balance": params.ACCOUNT_DEFAULT_BALANCE,
            "end_balance": self.net_worth(),
            "trade_history": self.history(),
            "performance": self.performance(),
            "metrics": self.metrics(),
        }

        # Return JSON Object
        return json
