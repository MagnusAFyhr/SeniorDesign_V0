"""

Title : experiment.py
Author : Magnus Fyhr
Created : 02/05/2020

Purpose :


Development :
    - init      :
    - run       :

Testing :
    - init      :
    - run       :

TO-DO:
    - implement run() method
    - implement system testing capability


Comments :


"""

from analysis.simulator import simulator as sim
import pandas as pd
import time


class Experiment(object):

    """
s    """
    def __init__(self, tickers, sample_size, debug=0):

        # Assign Tickers
        self.tickers = list([])
        if isinstance(tickers, list):
            self.tickers.extend(tickers)
        else:
            self.tickers = list([tickers])

        self.sample_size = sample_size
        self._debug_mode = debug

        return

    """
    Run Experiment; Run N Simulations
    """
    def run(self):

        # Header Message To Console
        print("< EXP > : Building experiments for {} tickers and sample size of {}".format(
            len(self.tickers),
            self.sample_size
        ))
        print("< EXP > : Tickers : {}".format(
            self.tickers,
        ))
        print()

        # Iterate Through Tickers To Be Tested
        est_sims = self.sample_size * len(self.tickers)
        sim_count = 0
        runtimes = list([])
        for index, ticker in enumerate(self.tickers):
            # Provide Some Feedbackc
            print("<     > : {} : Launching Stock Experiment...".format(
                ticker
            ))

            # Create Filename
            filename = "results/{}_results.csv".format(ticker)

            # Create List To Store All Samples' Results
            exp_results = None

            # Iteratively Run Simulations & Log Results
            for i in range(0, self.sample_size):

                sim_start_t = time.time_ns()
                # Create simulation
                simulation = sim.Simulator(ticker, sim_id=i, debug=self._debug_mode)
                # Run Simulation
                raw_sim_results = simulation.run()

                sim_end_t = time.time_ns()
                elapsed = sim_end_t - sim_start_t
                elapsed /= pow(10, 9)
                sim_count += 1
                runtimes.append(elapsed)

                # Reformat Generational Statistics
                for gen_i in range(1, len(raw_sim_results)):
                    gen_stat = raw_sim_results[gen_i]
                    # Format The Results To Fit A Pandas DataFrame
                    fmt_sim_results = {
                        "ticker": ticker,
                        "sim_id": i,

                        # general stats
                        "runtime": gen_stat["runtime"],
                        "pop_size": gen_stat["pop_size"],
                        "gen_count": gen_stat["gen_count"],
                        "open_date": gen_stat["open_date"],
                        "close_date": gen_stat["close_date"],
                        "open_price": gen_stat["open_price"],
                        "close_price": gen_stat["close_price"],

                        # market stats

                        # population fitness
                        "best_fit": gen_stat["best_fit"],
                        "worst_fit": gen_stat["worst_fit"],
                        "mean_fit": gen_stat["mean_fit"],
                        "std_fit": gen_stat["std_fit"],

                        # elite fitness
                        "best_elite_fit": gen_stat["best_elite_fit"],
                        "worst_elite_fit": gen_stat["worst_elite_fit"],
                        "mean_elite_fit": gen_stat["mean_elite_fit"],
                        "std_elite_fit": gen_stat["std_elite_fit"],

                        # detailed elite trade stats
                        "trade_count": gen_stat["elites_overall_stats"]["general"]["trade_count"],
                        "trade_net_earnings": gen_stat["elites_overall_stats"]["general"]["net_earnings"],
                        "trade_win_count": gen_stat["elites_overall_stats"]["general"]["win_count"],
                        "trade_net_gain": gen_stat["elites_overall_stats"]["general"]["net_gain"],
                        "trade_lose_count": gen_stat["elites_overall_stats"]["general"]["loss_count"],
                        "trade_net_loss": gen_stat["elites_overall_stats"]["general"]["net_loss"],

                        "long_count": gen_stat["elites_overall_stats"]["general"]["long"]["count"],
                        "long_net_earnings": gen_stat["elites_overall_stats"]["general"]["long"]["net_earnings"],
                        "long_win_count": gen_stat["elites_overall_stats"]["general"]["long"]["winners"]["count"],
                        "long_net_gain": gen_stat["elites_overall_stats"]["general"]["long"]["winners"]["net_gain"],
                        "long_lose_count": gen_stat["elites_overall_stats"]["general"]["long"]["losers"]["count"],
                        "long_net_loss": gen_stat["elites_overall_stats"]["general"]["long"]["losers"]["net_loss"],

                        "short_count": gen_stat["elites_overall_stats"]["general"]["short"]["count"],
                        "short_net_earnings": gen_stat["elites_overall_stats"]["general"]["short"]["net_earnings"],
                        "short_win_count": gen_stat["elites_overall_stats"]["general"]["short"]["winners"]["count"],
                        "short_net_gain": gen_stat["elites_overall_stats"]["general"]["short"]["winners"]["net_gain"],
                        "short_lose_count": gen_stat["elites_overall_stats"]["general"]["short"]["losers"]["count"],
                        "short_net_loss": gen_stat["elites_overall_stats"]["general"]["short"]["losers"]["net_loss"],

                        # detailed elite performance stats
                        "profit_factor": 0,
                        "gain_to_pain": 0,
                        "winning_pct": 0,
                        "payout_ratio": 0,
                        "cpc_index": 0,
                        "expectancy": 0,
                        "return_pct": 0,
                        "kelly_pct": 0,
                        "sharpe": 0,
                        "treynor": 0,
                        "sortino": 0,
                    }

                    # Log Results To Pandas DataFrame
                    if exp_results is None:
                        exp_results = fmt_sim_results
                        for key, value in exp_results.items():
                            exp_results[key] = list([value])
                    else:
                        for key, value in fmt_sim_results.items():
                            exp_results[key].append(value)

                # calculate various runtime stats
                sum_time = sum(runtimes)
                avg_time = sum_time / len(runtimes)
                percent_complete = round((sim_count / est_sims) * 100, 3)
                est_time = round(avg_time * (est_sims - sim_count), 3)
                # Provide Feedback
                print("< EXP > : Experiment {}% Complete. {} Seconds Until Completion. ({} s)".format(
                    percent_complete,
                    est_time,
                    elapsed
                ))
                # Advance To Next Simulation
                continue

            # Convert List To Pandas DataFrame
            pandas_sim_results = pd.DataFrame.from_dict(exp_results, 'columns')

            # Write Pandas DataFrame To CSV File Within New Directory
            pandas_sim_results.to_csv(filename, sep=',', encoding='utf-8', index=False)

            # Provide Some Feedback
            print("<     > : {} : Stock Experiment Complete; Check Results Directory! ({}/{})".format(
                ticker,
                index, len(self.tickers)
            ))
            # Advance To Next Ticker
            continue

        # Provide Some Feedback
        print("< EXP > : Experiment Fully Complete; Check Results Directory!")

        # Done; Experiment Complete!
        return






