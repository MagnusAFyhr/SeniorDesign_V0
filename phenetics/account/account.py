"""

Title : chromosome.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : The Account class object, responsible for providing proper
            functions and expected functionality for trading any
            given stock.

Development :
    - init          :
    - verify        :
    - long          :
    - short         :
    - balance       :
    - net_worth     :
    - history       :
    - performance   :
    - statistics    :

Testing :
    - init          :
    - verify        :
    - long          :
    - short         :
    - balance       :
    - net_worth     :
    - history       :
    - performance   :
    - statistics    :

"""


class Account(object):

    trade_history = [None] * 100

    # Initialization
    def __init__(self, ticker):
        self.stock_tick = ticker


    def verify(self):
        pass

    # Simulates a buy order, resets short position
    def long(self, timestamp, price):
        pass

    # Simulates sell order, resets long position, calculates money earned from buy and sell.
    def short(self, timestamp, price):
        pass

    # Returns the current free capital available to invest
    def balance(self):
        return self.balance

    # Calculates the net value of all current assets and balance
    def netWorth(self):
        pass

    # WHAT DO I DO
    def history(self):
        pass

    # Calculates some metric for the accuracy of the individuals decisions
    def performance(self):
        pass

    # Calculates several metrics for the accounts behavior
    def statistics(self):
        pass
