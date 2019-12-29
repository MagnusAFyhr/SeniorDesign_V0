"""

Title : habitat.py
Author : Magnus Fyhr
Created : 12/17/2019

Purpose : The Habitat class object, responsible for simulating data
            to a generationally adapting Population; data is simulated
            in time-series. Controls the

Development :
    - init              : (ticker)
    - simulate          :
    - plot              :

Testing :
    - init              :
    - step              :



"""

# 251 trading days per year
MAX_GEN = 40        # 40 generations; 2000 days of data; ~8 years of historical data
GEN_PERIOD = 50     # 50 days of trading
POP_SIZE = 1000     # 1,000 individuals


class Habitat:

    def __init__(self, ticker):

        # load ticker data

        self.population = None

        return

    def simulate_generation(self):

        for t in range(0, GEN_PERIOD):
            observation = None
            self.population.step(observation)

        gen_stats = self.population.next_generation()

        return gen_stats

    def plot(self):
        pass
