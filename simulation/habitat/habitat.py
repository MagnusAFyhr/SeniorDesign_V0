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



"""

import simulation.population.population as popu
import data.driver.databook as data
import time

# 251 trading days per year
MAX_GEN = 40        # 40 generations; 2000 days of data; ~8 years of historical data
GEN_PERIOD = 50     # 50 days of trading
POP_SIZE = 1000     # 1,000 individuals


class Habitat:

    def __init__(self, ticker):

        # load ticker data
        self.environment = data.DataBook(ticker)

        # initialize random population
        self.population = popu.Population(POP_SIZE)

        return

    def simulate_generation(self):

        start = time.time_ns()

        for t in range(0, GEN_PERIOD):
            observation = self.environment.step()
            self.population.step(observation)

        gen_stats = self.population.next_generation()

        end = time.time_ns()
        elapsed = end - start
        elapsed /= pow(10, 9)
        gen_stats["runtime"] = elapsed

        self.plot(gen_stats)

        return gen_stats

    def plot(self, gen_stats):
        # print generation stats to debug console
        print("< SYS > : Generation {}; Runtime : {} sec.".format(gen_stats["gen_count"], gen_stats["runtime"]))
        print("<     > : Duration: {} :: {} ({} ticks).".format(gen_stats["start_date"],
                                                                gen_stats["end_date"],
                                                                gen_stats["step_count"]))
        print("<     > : Sum Fitness : {}.".format(gen_stats["sum"]))
        print("<     > : Best : {}, Worst : {}, Mean : {}.".format(gen_stats["best"],
                                                                   gen_stats["worst"],
                                                                   gen_stats["mean"]))
        print("<     > : Stand. Dev. : {}.".format(gen_stats["std"]))
        print("")

        # do visualization stuff

        pass
