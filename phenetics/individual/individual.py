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
    - as_json       : DONE

"""

import genetics.chromosome.chromosome as chrm
import phenetics.account.account as acco


class Individual:

    """
    Initialize & Verify The Individual
    """
    def __init__(self, chromosome=None):

        # Verify The Chromosome
        if chromosome is None:
            chromosome = chrm.Chromosome()

        if not chromosome.initialized:
            print("< ERR > : Failed to initialize Individual, used invalid Chromosome!")
            self.initialized = False
            return

        # Initialize The Individual
        self.initialized = False
        self.asset = "AAPL"
        self.chromosome = chromosome
        self.account = acco.Account(self.asset)

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

        elif not self.chromosome.initialized:
            return False

        # Verify Account
        if self.account is None:
            return False

        elif not self.account.initialized:
            return False

        # Otherwise, Individual Is Verified
        return True

    """
    Simulates The Next Step In The Data
    """
    def step(self, row_dict):
        # Extract the price and timestamp from the dictionary
        timestamp = row_dict["Date"]
        price = row_dict["Close"]

        if price is None or timestamp is None:
            print("< ERR > : Error in Individual step(), Invalid Data Dictionary.")
            return None

        # Get the reaction from the chromosome
        reaction = self.chromosome.react(row_dict)

        # Use the reaction to take action via do()
        feedback = self.account.do(reaction, timestamp, price)

        # Done
        return feedback

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
    Returns Two Offspring Chromosomes From Mating Two Individuals
    """
    def mate(self, mate):
        # Obtain two chromosomes from mating two individuals
        chrom_encodings = self.chromosome.crossover(mate.chromosome)

        # Create chromosomes from encoding
        offspring = list([])
        for encoding in chrom_encodings:
            offspring.append(chrm.Chromosome(encoding))

        # Return Chromosome Objects
        return offspring

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

        # Format Individual object into JSON object
        json = {
            "init": self.initialized,
            "asset": self.asset,
            "chromosome": self.chromosome.as_string(),
            "account": self.account.as_json(),
        }

        # Return JSON object
        return json




