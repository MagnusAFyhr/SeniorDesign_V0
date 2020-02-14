"""

Title : habitat.py
Author : Magnus Fyhr
Created : 1/7/2020

Purpose : The Habitat class object, responsible for simulating data
            to a generationally adapting Population; data is simulated
            in time-series. Controls the...

Development :
    - init                          : DONE
    - simulate_generation           : DONE
    - report                        :
    - status                        :
    - plot                          :

Testing :
    - init                          :
    - simulate_generation           :
    - report                        :
    - status                        :
    - plot                          :

Cleaning :
    - init                          : DONE
    - simulate_generation           : DONE
    - report                        :
    - status                        :
    - plot                          :

Optimizing :
    - init                          :
    - simulate_generation           :
    - report                        :
    - status                        :
    - plot                          :


TO-DO:
    - improve report() function
        + add more to it; need financial part too
        + clean it up
    - add status() function
    - Add logic to track movement of price over a generation; should account do this


"""

import analysis.parameters as params

import simulation.population.population as popu
import data.driver.databook as data

import time


class Habitat:

    """
    Initialize Habitat
    """
    def __init__(self, ticker, debug=0):

        # Pre-Initialization
        self.initialized = False
        self._debug_mode = 0
        self._is_debug = False

        self.environment = None
        self.population = None

        # Setup Debug Mode
        self._debug_mode = debug
        if self._debug_mode in params.HABITAT_DEBUG:
            self._is_debug = True

        # Initialize & Verify DataBook
        self.environment = data.DataBook(ticker, params.GEN_PERIOD, gen_count=params.GEN_COUNT)
        if not self.environment.initialized:
            print("< ERR > :{} Failed to initialize Habitat; DataBook failed verification!")
            return

        # Initialize Population
        self.population = popu.Population(params.POP_SIZE, debug=self._debug_mode)
        if not self.population.initialized:
            print("< ERR > :{} Failed to initialize Habitat; Population failed verification!")
            return

        # Initialization Complete!
        self.initialized = True
        return

    """
    Simulate A Generation For The Population
    """
    def simulate_generation(self):

        # WHAT IS THIS
        if self._is_debug or self._debug_mode in params.HABITAT_CONSOLE:
            print("\t< HAB > : Simulating Generation {}...".format(self.population.gen_count))

        # Begin Simulation Timer
        start = time.time_ns()

        # Simulate N Days Of Data Across Population (N=GEN_PERIOD)
        for t in range(0, params.GEN_PERIOD):
            # obtain data for subsequent day
            observation = self.environment.step()

            # sanity check; make sure nothing has gone wrong
            if observation == "EOF" or observation is None:
                return None

            # commence the simulation of the single observation
            self.population.step(observation)

        # Initialize Next Generation; Also Obtain Statistics From Previous Generation
        gen_stats = self.population.next_generation()

        # Make Sure Simulation Went Well
        if gen_stats is None:
            print("< ERR > : Habitat : Failed to simulate generation; Population failed to create next generation!")
            return None

        # End Simulation Timer; Calculate Elapsed Time
        end = time.time_ns()
        elapsed = end - start
        elapsed /= pow(10, 9)
        gen_stats["runtime"] = elapsed

        if self._is_debug or self._debug_mode in params.HABITAT_CONSOLE:
            print("\t< HAB > : Generational Simulation Complete!")

        # Print Generational Statistics To Console;
        self.report(gen_stats)

        # Generation Simulation Complete; Return Generational Statistics!
        return gen_stats

    """
    Print Generation Stats To Debug Console
    """
    def report(self, gen_stats):

        if self._debug_mode in params.HABITAT_CONSOLE:
            # Generic Header
            print("\t\t<     > : Generation\t\t\t\t\t: {} ".format(gen_stats["gen_count"]))
            print("\t\t<     > : Population Size\t\t\t\t: {}".format(gen_stats["pop_size"]))
            print("\t\t<     > : Runtime\t\t\t\t\t\t: {} seconds".format(round(gen_stats["runtime"], 4)))
            print("\t\t<     > : Start Date\t\t\t\t\t: {} ".format(gen_stats["start_date"]))
            print("\t\t<     > : End Date\t\t\t\t\t\t: {} ".format(gen_stats["end_date"]))
            print("\t\t<     > : Duration\t\t\t\t\t\t: {} days".format(gen_stats["step_count"]))

            # General Statistics
            print("\t< HAB > : General Statistics. ")
            print("\t\t<     > : Best Fitness\t\t\t\t\t: {}".format(round(gen_stats["best_fit"], 4)))
            print("\t\t<     > : Mean Fitness\t\t\t\t\t: {}".format(round(gen_stats["mean_fit"], 4)))
            print("\t\t<     > : Worst Fitness\t\t\t\t\t: {}".format(round(gen_stats["worst_fit"], 4)))
            print("\t\t<     > : Fitness Std. Dev.\t\t\t\t: {}".format(round(gen_stats["fit_stdev"], 4)))
            print("\t\t<     > : Allele Diversity\t\t\t\t: {}%".format(round(gen_stats["allele_sdi"] * 100, 2)))
            print("\t\t<     > : Chromosome Diversity\t\t\t: {}%".format(round(gen_stats["chrom_sdi"] * 100, 2)))

        # Performance Statistics
        if self._debug_mode in params.ACCOUNT_CONSOLE:
            print("\t< HAB > : Performance Statistics. ")
            print("\t\t<     > : Put")
            print("\t\t<     > : Stuff")
            print("\t\t<     > : Here...")

        # Done Reporting!
        return

    """
    Returns Dictionary Representation Of Habitat's Current State
    """
    def status(self):
        #
        pass


    """
    Provide Runtime Visualizations
    """
    def plot(self):
        # do visualization stuff
        pass
