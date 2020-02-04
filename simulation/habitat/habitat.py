"""

Title : habitat.py
Author : Magnus Fyhr
Created : 1/7/2020

Purpose : The Habitat class object, responsible for simulating data
            to a generationally adapting Population; data is simulated
            in time-series. Controls the

Development :
    - init              :
    - simulate          :
    - plot              :

Testing :
    - init              :
    - simulate          :
    - plot              :

TO-DO:
    - allow MAX_GEN, GEN_PERIOD, & POP_SIZE to be manipulated by some higher-level analytics class : DONE
    - add verify() method?

"""

import analysis.parameters as params

import simulation.population.population as popu
import data.driver.databook as data

import time

# 251 trading days per year
# MAX_GEN = 40        # 40 generations; 2000 days of data; ~8 years of historical data
# GEN_PERIOD = 50     # 50 days of trading
# POP_SIZE = 1000     # 1,000 individuals


class Habitat:

    initialized = False
    _debug_mode = 0

    environment = None
    population = None

    def __init__(self, ticker, debug=0):  # gen_period, days_of_sim=None, start_date=None, end_date=None

        self._debug_mode = debug

        # load ticker data
        self.environment = data.DataBook(ticker, params.GEN_PERIOD)

        # initialize random population
        self.population = popu.Population(params.POP_SIZE, debug=self._debug_mode)

        # Done Initializing
        self.initialized = True
        return

    def simulate_generation(self):

        if self._debug_mode > 0:
            print("\t< HAB > : Simulating Generation {}...".format(self.population.gen_count))

        # begin generation timer
        start = time.time_ns()

        # perform simulation
        for t in range(0, params.GEN_PERIOD):
            observation = self.environment.step()

            if observation == "EOF" or observation is None:
                return None

            self.population.step(observation)

        # obtain generational statistics of population
        gen_stats = self.population.next_generation()

        end = time.time_ns()
        elapsed = end - start
        elapsed /= pow(10, 9)
        gen_stats["runtime"] = elapsed

        # print generational statistics to console
        if self._debug_mode > 0 and self._debug_mode != 5:
            self.report(gen_stats)

        # Done; return generation statistics
        return gen_stats

    """
    Print Generation Stats To Debug Console
    """
    def report(self, gen_stats):  # IMPROVE THIS

        # Header
        print("\t< HAB > : Generation {} Simulated In {} Seconds.".format(
            gen_stats["gen_count"],
            round(gen_stats["runtime"], 4)
        ))

        # Computation Statistics
        print("\t\t<     > : Timeline : {} -> {}. ({} ticks)".format(
            gen_stats["start_date"], gen_stats["end_date"], gen_stats["step_count"]
        ))

        # Population Statistics
        print("\t\t<     > : Pop. Size : {}.".format(gen_stats["pop_size"]))
        print("\t\t<     > : Best : {}, Worst : {}, Mean : {}.".format(
            round(gen_stats["best"], 4),
            round(gen_stats["worst"], 4),
            round(gen_stats["mean"], 4)
        ))
        print("\t\t<     > : Stand. Dev. : {}.".format(
            round(gen_stats["std"], 4)
        ))

        # Allele Diversity Statistics
        print("\t\t<     > : Allele Diversity : {}%, {}:{}. (used:unused)".format(
            round(gen_stats["diversity"]["percent"], 2),
            gen_stats["diversity"]["used"],
            gen_stats["diversity"]["unused"]
        ))
        print("\t\t\t\t\tHigh : {} ({}%),\n\t\t\t\t\tLow : {} ({}%),\n\t\t\t\t\tMean : {} ({}%)".format(
            gen_stats["diversity"]["high"],
            round(100 * gen_stats["diversity"]["high"] / gen_stats["diversity"]["sum"], 2),
            gen_stats["diversity"]["low"],
            round(100 * gen_stats["diversity"]["low"] / gen_stats["diversity"]["sum"], 2),
            round(gen_stats["diversity"]["mean"], 2),
            round(100 * gen_stats["diversity"]["mean"] / gen_stats["diversity"]["sum"], 2)
        ))
        print("\t\t\t\t\tStand. Dev. : {}.".format(
            round(gen_stats["diversity"]["std"], 4)
        ))

        # Done
        return

    """
    Provide Runtime Visualizations
    """
    def plot(self):
        # do visualization stuff
        pass
