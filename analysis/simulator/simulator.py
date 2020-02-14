"""

Title : simulator.py
Author : Magnus Fyhr
Created : 01/26/2020

Purpose :


Development :
    - init ()           : DONE
    - run()             : DONE

Testing :
    - init ()           :
    - run()             :

Cleaning :
    - init()            : DONE
    - run()             : DONE

Optimizing :
    - init ()           :
    - run()             :

TO-DO:

Comments :

"""


from simulation.habitat import habitat as habi
from analysis import parameters as params

import time


class Simulator(object):

    """
    Initialize & Verify The Simulator
    """
    def __init__(self, ticker, sim_id="", debug=0):

        # Pre-Initialization
        self.initialized = False
        self._debug_mode = 0

        self.sim_id = ""
        self.ticker = ""
        self.habitat = None

        # Setup Debug Mode
        self._debug_mode = debug

        # Assign Simulation ID
        if sim_id != "":
            self.sim_id = " [{}] :".format(sim_id)

        # Assign Ticker
        self.ticker = ticker

        # Initialize & Verify Habitat
        self.habitat = habi.Habitat(ticker, debug=self._debug_mode)
        if not self.habitat.initialized:
            print("< ERR > :{} Failed to initialize Simulator; Habitat failed verification!")
            return

        # Done Initializing
        self.initialized = True
        return

    """
    Run Simulation
    """
    def run(self):

        # Sanity Check
        if not self.initialized:
            return

        # Header Message To Console
        print("< SIM > :{} Beginning simulation of {} historical data from {} to {}.".format(
            self.sim_id,
            self.ticker,
            self.habitat.environment.start_date,
            self.habitat.environment.end_date
        ))

        # Extended Header Message To Console
        sim_length = len(self.habitat.environment.book.index)
        est_gens = int(sim_length / params.GEN_PERIOD)
        if self._debug_mode in params.SIMULATION_CONSOLE:
            print("< SIM > :{} Simulating population of size {} across {} days of trading data.".format(
                self.sim_id,
                self.habitat.population.size,
                sim_length
            ))
            print("< SIM > :{} Simulating {} generations using generation period of {} days.".format(
                self.sim_id,
                est_gens,
                params.GEN_PERIOD
            ))

        # Create Empty List To Store Generation Runtimes
        sim_stats = list([])

        # Perform Simulation; Log Statistics To 'gen_stats'
        runtimes = list([])
        sim_start_t = time.time_ns()
        while self.habitat.population.gen_count < est_gens:
            # simulate a generation
            gen_stats = self.habitat.simulate_generation()

            # handle bad generation
            if gen_stats is None:
                print("< ERR > :{} Simulator : Failed to simulate generation {}; generation stats were NoneType!".format(
                    self.sim_id,
                    self.habitat.population.gen_count
                ))
                return None

            # append runtime statistics to list
            runtimes.append(gen_stats["runtime"])

            # append generation statistics to list
            sim_stats.append(gen_stats)

            # provide runtime feedback
            if self._debug_mode in params.SIMULATION_CONSOLE:
                # calculate various runtime stats
                sum_time = sum(runtimes)
                avg_time = sum_time / len(runtimes)
                percent_complete = round((self.habitat.population.gen_count / est_gens) * 100, 3)
                est_time = round(avg_time * (est_gens - self.habitat.population.gen_count), 3)
                # print to console
                print("< SIM > :{} Simulation {}% complete. {} seconds until completion. ({} s)".format(
                    self.sim_id,
                    percent_complete,
                    est_time,
                    gen_stats["runtime"]
                ))

        # Footer Message To Console; Completion Feedback
        sim_end_t = time.time_ns()
        elapsed = sim_end_t - sim_start_t
        elapsed /= pow(10, 9)
        print("< SIM > :{} Simulation complete! Simulated in {} seconds.".format(
            self.sim_id,
            elapsed
        ))

        # Return Array Of Generation Stats; Array Of Dictionaries
        return sim_stats

