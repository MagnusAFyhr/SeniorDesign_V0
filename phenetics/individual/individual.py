"""

Title : individual.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : The Chromosome class object, responsible for providing proper
            functions and expected functionality for the Chromosome.

Development :
    - init          : DONE
    - verify        : DONE
    - step          : DONE
    - fitness       : DONE
    - mate          : DONE
    - clone         : DONE
    - as_json       : DONE

Testing :
    - init          : DONE
    - verify        : DONE
    - step          : DONE
    - fitness       : DONE
    - mate          : DONE
    - clone         : DONE
    - status        : DONE

Cleaning :
    - init          : DONE
    - verify        : DONE
    - step          : DONE
    - fitness       : DONE
    - mate          : DONE
    - clone         : DONE
    - status        : DONE

Optimizing :
    - init          :
    - verify        :
    - step          :
    - fitness       :
    - mate          :
    - clone         :
    - status        :


TO-DO:

Comments :

Future Improvements :


"""

import genetics.chromosome.chromosome as chrm
import phenetics.account.account as acco
import analysis.parameters as params


class Individual:

    """
    Initialize & Verify The Individual
    """
    def __init__(self, ticker="", chromosome=None, debug=0):

        # Pre-Initialization
        self.initialized = False
        self._debug_mode = 0
        self._is_debug = False

        self.ticker = ticker
        self.chromosome = None
        self.account = None

        # Setup Debug Mode
        self._debug_mode = debug
        if debug in params.INDIVIDUAL_DEBUG:
            self._is_debug = True

        # Check Chromosome
        if chromosome is None:
            chromosome = chrm.Chromosome(debug=self._debug_mode)

        # Initialize The Individual
        self.ticker = ticker
        self.chromosome = chromosome
        self.account = acco.Account(ticker=self.ticker, debug=self._debug_mode)

        # Verify The Individual
        if self._is_debug:
            if self.verify() is False:
                print("< ERR > : Failed to initialize Individual; verification failed!")
                return

        # Initialization Complete!
        self.initialized = True
        return

    """
    Verifies The Initialization Of An Individual
    """
    def verify(self):
        # Verify Chromosome
        if self.chromosome is None:
            return False

        elif not self.chromosome.initialized:
            return False

        # Verify Account
        if self.account is None:
            return False

        elif not self.account.initialized:
            return False

        # Verification Complete!
        return True

    """
    Simulates The Next Step In The Data
    """
    def step(self, row_dict):
        # Extract The Price & Timestamp From The Dictionary
        timestamp = row_dict["Date"]
        price = row_dict["Close"]

        if self._is_debug:
            if price is None or timestamp is None:
                print("< ERR > : Error in Individual step(), Invalid Data Dictionary.")
                return None

        # Get The Reaction From The Chromosome
        reaction = self.chromosome.react(row_dict)

        if self._is_debug:
            if reaction is None:
                print("< ERR > : NoneType action received from Chromosome react() : {}.".format(reaction))

        # Use The Reaction To Take Action Via 'do()' Command; Obtain Feedback
        feedback = self.account.do(reaction, timestamp, price)

        if self._is_debug:
            if feedback is None:
                print("< ERR > : NoneType feedback received from Account do() : {}.".format(feedback))

        # Step Complete!
        return feedback

    """
    Calculates The Fitness Of An Individual
    """
    def fitness(self):
        # Obtain Account Performance As Individual Fitness
        fitness = self.account.performance()

        # Return Fitness
        return fitness

    """
    Returns Two Offspring Chromosomes From Mating Two Individuals
    """
    def mate(self, mate):
        # Obtain Two Chromosomes From Mating Two Individuals
        chrom_encodings = self.chromosome.crossover(mate.chromosome)

        # Create Chromosomes From Encoding
        offspring = list([])
        for encoding in chrom_encodings:
            offspring.append(chrm.Chromosome(encoding=encoding, debug=self._debug_mode))

        # Mating Complete; Return Initialized Chromosomes!
        return offspring

    """
    Returns A Copy Of The Individual’s Chromosome
    """
    def clone(self):
        return self.chromosome

    """
    Returns Dictionary Representation Of Individual's Current State
    """
    def status(self):
        # Format Individual Into Dictionary Object
        state = {
            "init": self.initialized,
            "asset": self.ticker,
            "chromosome": self.chromosome.status(),
            "account": self.account.status(),
        }

        # Return Dictionary Object
        return state




