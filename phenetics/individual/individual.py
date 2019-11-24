"""

Title : chromosome.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : The Chromosome class object, responsible for providing proper
            functions and expected functionality for the Chromosome.

Development :
    - init          : Should the individual be initialized with a chromosome or an encoding
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
import phenetics.account.account as acco


class Individual(object):

    """
    Initialize & Verify The Individual
    """
    def __init__(self, chromosome=None):

        # Verify The Chromosome
        if chromosome is None:
            chromosome = chrm.Chromosome()

        elif not chromosome.initialized:
            print("< ERR > : Failed to initialize Individual, invalid Chromosome!")
            self.initialized = False
            return

        # Initialize The Individual
        self.initialized = False
        self.chromosome = chromosome
        self.account = acco.Account("AAPL")

        # Verify The Individual
        if self.verify() is False:
            print("< ERR > : Failed to initialize Individual, verification failed!")
            return

        # Done Initializing
        self.initialized = True
        return

    """
    Verifies The Initialization Of An Individual
    """
    def verify(self):
        # Verify Chromosome
        if self.chromosome is None:
            return False

        # Verify Account
        if self.account is None:
            return False

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
    def step(self, row_dict):

        # Get the reaction from the chromosome
        reaction = self.chromosome.react(row_dict)

        # Use the reaction to take action via do()
        self.do(reaction)

        # Handle do results
        print("step() : ")

    """
    Calculates The Fitness Of An Individual
        - fitness should be a dictionary of buy_performance, sell_performance, etc.
        - for now fitness will just be performance
    """
    def fitness(self):
        # Obtain fitness from account performance
        fitness = self.account.performance()

        # Return fitness
        return fitness

    """
    Returns Two Offspring Encodings From Mating Two Individuals
    """
    def mate(self, mate):
        # Obtain two chromosomes from mating two individuals, and return them
        return self.chromosome.crossover(mate.chromosome)

    """
    Returns A Copy Of The Current Individual’s Chromosome
    """
    def clone(self):
        # Return copy of individual's chromosome
        return self.chromosome

    """
    Return A Summary Of The Individual As A JSON Object
    """
    def as_json(self):
        print("Individual to json function")
        return




