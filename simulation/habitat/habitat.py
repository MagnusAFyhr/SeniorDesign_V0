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
    - status                        : DONE
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

COMMENTS:
    - "params.AVAIL_TECH_IND = self.environment.tech_ind_dict"; new approach should be used

"""

from simulation.habitat.helper import habitat_console_logger as console

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

        self.ticker = ticker

        self.environment = None
        self.population = None

        # Setup Debug Mode
        self._debug_mode = debug
        if self._debug_mode in params.HABITAT_DEBUG:
            self._is_debug = True

        # Initialize & Verify DataBook
        self.environment = data.DataBook(ticker, params.GEN_PERIOD, gen_count=params.GEN_COUNT)
        if not self.environment.initialized:
            print("< ERR > : Habitat : {} Failed to initialize Habitat; DataBook failed verification!")
            return

        # Update Global Variable For Available Technical Indicators; Used By Alleles
        params.AVAIL_TECH_IND = self.environment.tech_ind_dict

        # Initialize Population
        self.population = popu.Population(params.POP_SIZE, debug=self._debug_mode)
        if not self.population.initialized:
            print("< ERR > : Habitat : {} Failed to initialize Habitat; Population failed verification!")
            return

        # Initialization Complete!
        self.initialized = True
        return

    """
    Simulate A Generation For The Population
    """
    def simulate_generation(self):

        # Beginning Debug Reporting
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

        # Completion Debug Reporting
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

        console.report(gen_stats, self._debug_mode)

        # Done Reporting!
        return

    """
    Returns Dictionary Representation Of Habitat's Current State; Useful For System Testing
    """
    def status(self):
        # Format Habitat Into Dictionary Object
        state = {
            "init": self.initialized,
            "debug_mode": self._debug_mode,
            "is_debug": self._is_debug,

            "ticker": self.ticker,

            "environment": self.environment,
            "population": self.population
        }

        # Return Dictionary Object
        return state

    """
    Provide Runtime Visualizations
    """
    def plot(self):
        # do visualization stuff
        pass
