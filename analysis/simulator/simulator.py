"""

Title : simulator.py
Author : Magnus Fyhr
Created : 01/26/2020

Purpose :


Development :


Testing :


TO-DO:
    - Implement function to log simulation stats
    - Pre-Simulation Debug Console Header
    - Need Support For Experiment; if we want to simulate multiple habitats at the same time.

"""


from simulation.habitat import habitat as habi
from analysis import parameters as params

import time


class Simulator(object):

    initialized = False
    _debug_mode = 0

    ticker = ""
    habitat = None

    """
    Initialize & Verify The Simulator
    """
    def __init__(self, ticker, debug=0):

        self._debug_mode = debug

        self.ticker = ticker

        # Create Habitat
        self.habitat = habi.Habitat(ticker, debug=self._debug_mode)

        # Verify The Simulator
        if self._debug_mode:
            pass

        # Done Initializing
        self.initialized = True
        return

    """
    Perform Simulation
    """
    def run_simulation(self):

        sim_length = self.habitat.environment.book.shape[0]
        est_gens = sim_length / params.GEN_PERIOD
        print("< SIM > : Beginning simulation; Estimated {} Generations Using {} Days Of {} Trading Data.".format(
            est_gens, sim_length, self.ticker
        ))

        # Create empty array to store runtime generation stats
        gen_stats = list([])

        # Perform simulation; log statistics
        runtimes = list([])
        sim_start_t = time.time_ns()
        while self.habitat.population.gen_count < params.MAX_GEN:
            # Simulate a generation
            this_gen_stats = self.habitat.simulate_generation()
            runtimes.append(this_gen_stats["runtime"])

            # Provide generation feedback
            if self._debug_mode > 0:
                if this_gen_stats is None or this_gen_stats == "EOF":
                    # Handle bad generation
                    pass

            gen_stats.append(this_gen_stats)

            # Provide runtime feedback
            sum_time = sum(runtimes)
            avg_time = sum_time / len(runtimes)
            percent_complete = round((self.habitat.population.gen_count / est_gens) * 100, 3)
            est_time = round(avg_time * (est_gens - self.habitat.population.gen_count), 3)
            print("< SIM > : Simulation {}% complete. {} seconds until completion. ({} s)".format(
                percent_complete, est_time, this_gen_stats["runtime"]
            ))

        # Provide completion feedback
        sim_end_t = time.time_ns()
        elapsed = sim_end_t - sim_start_t
        print("< SIM > : Simulation complete! Simulated in {} seconds.".format(elapsed))

        # Return array of runtime generation stats; array of dictionaries
        return gen_stats

