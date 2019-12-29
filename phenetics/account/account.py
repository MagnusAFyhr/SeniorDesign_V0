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
    - statistics    :
    - as_json       : DONE

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
    - statistics    :
    - as_json       : DONE


Need to add streak along with cool down
SHARPE RATIO FOR FITNESS

"""


class Account(object):

    def_volume = 1000
    def_balance = 10000.00
    def_trade_cool_down = 3

    """
    Initialize & Verify The Account
    """
    def __init__(self, ticker):

        # Initialize The Account
        self.initialized = False

        self.ticker = ticker

        self.trade_history = list([])
        self.curr_position = None
        self.curr_balance = self.def_balance
        # trade_volume = 0

        self.curr_cool_down = 0
        self.curr_streak = 0

        self.last_update = None
        self.last_price = None

        # Make Default Current Position As A JSON Object
        self.curr_position = {
            "action": "",
            "price": 0,
            "quantity": 0,
        }

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
        if self.ticker is None:
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
            success = self.long(timestamp, price, self.def_volume)
            return success

        elif action == "SELL":
            # Enter short position, if possible
            success = self.short(timestamp, price, self.def_volume)
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
    Calculates The ROI Of An Account; Used By Individual For Fitness
    """
    def performance(self):
        # Calculate ROI based on accounts net worth and starting balance
        roi = self.net_worth() / self.def_balance

        # Return the ROI
        return roi

    """
    Returns Several Metrics Of The Accounts Behavior As A JSON Object
    """
    def statistics(self):
        pass

    """
    Return A Summary Of The Account As A JSON Object
    """
    def as_json(self):

        # Format Account object into JSON object
        json = {
            "init": self.initialized,
            "stock": self.ticker,
            "start_balance": self.def_balance,
            "end_balance": self.curr_balance,
            "net_worth": self.net_worth(),
            "performance": self.performance(),
            "statistics": self.statistics(),
        }

        # Return JSON object
        return json
