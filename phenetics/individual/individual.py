"""

Title : chromosome.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : The Chromosome class object, responsible for providing proper
            functions and expected functionality for the Chromosome.

Development :
    - init          :
    - verify        :
    - do            :
    - step          :
    - fitness       :
    - mate          :
    - clone         :
    - as_string     :

Testing :
    - init          :
    - verify        :
    - do            :
    - step          :
    - fitness       :
    - mate          :
    - clone         :
    - as_string     :

"""

import genetics.chromosome.chromosome as chrm
from genetics.chromosome.helper import chrom_build as chr_bui


class Individual(object):
    """
    Initialize & Verify The Individual
    """

    def __init__(self, encoding=None):
        if encoding is None:
            encoding = chr_bui.random_encoding()

        # Initialize The Individual
        self.initialized = False
        self.encoding = encoding
        self.chromosome = chrm.Chromosome(encoding)
        # self.account = account.Account()

        # Verify The Individual
        if self.verify() is False:
            print("< ERR > : Failed to verify individual!\n")
            return

        self.initialized = True
        return

    """
    Verifies The Initialization Of An Individual
    """
    def verify(self):
        # Verify Genotype
        if self.encoding is None:
            return False

        # Verify Account
        #if self.account is None:
        #    return False

        # Otherwise, Individual Is Verified
        return True

    """
    Attempts To Execute The Specified Action
    """
    def do(self, action):  # maybe add "WANT_BUY" "WANT_SELL"

        if action == "BUY":
            # BUY : buy 'trade_amount' of asset if ok

            # Do not allow individual to buy if cooldown active

            # Do not allow individual to buy if insufficient balance
            print("do() : BUY")

        elif action == "SELL":
            # SELL : sell current position of asset, short 'trade_amount' of asset

            # Do not allow individual to short if cooldown is active

            # Do not allow individual to short if insufficient balance
            print("do() : SELL")

        elif action == "HOLD":
            # HOLD : do nothing
            print("do() : HOLD")

        elif action is None:
            # Handle NoneType
            print("do() : Handle NoneType")

        else:
            # Handle Unrecognized Action
            print("do() : Unrecognized Action")


    """
    Simulates The Next Step In The Data
    """
    def step(self, data_dict):

        # Get the reaction from the chromosome

        # Use the reaction to take action via do()

        # Handle do results
        print("step() : ")

    """
    Calculates The Fitness Of An Individual
        - fitness should be a dictionary of buy_performance, sell_performance, etc.
    """
    def fitness(self):
        # Obtain fitness from account performance
        fitness = self.account.performance()

        # Return fitness
        return fitness

    """
    Returns N Children Between This Individual And A Given Mate
        - probably won't be used once gene pool is implemented
    """

    def mate(self, mate):  # , n_offspring):
        # Obtain two genotypes from mating two individuals, and return them
        return self.chromosome.crossover(self.chromosome, mate.chromosome)

    """
    Returns A Copy Of The Current Individual’s Encoding
    """
    def clone(self):
        # Return Copy Of Encoding
        return self.encoding

    """
    Return A Summary Of The Individual As A JSON Object
    """
    def as_string(self):
        print("log function")
        return




