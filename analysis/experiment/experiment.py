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


class Experiment(object):

    """
    Initialize & Verify The Experiment
    """
    def __init__(self, tickers, sample_size, debug=0):

        # Assign Tickers
        self.tickers = list([])
        if isinstance(tickers, list):
            self.tickers.extend(tickers)

        self.sample_size = sample_size

        return

    """
    Run Experiment; Run N Simulations
    """
    def run(self):

        # Provide Some Feedback

        # Create Directory Name

        # Create A New Directory Somewhere To Store All The Result Files To

        # Iterate Through Tickers To Be Tested
        for ticker in self.tickers:
            # Create Filename

            # Create Pandas DataFrame To Store All Samples' Results

            # Iteratively Run Simulations & Log Results
            for i in range(0, self.sample_size):
                # Run Simulation

                # Format The Results To Fit A Pandas DataFrame

                # Log Results To Pandas DataFrame

                # Provide Some Feedback

                # Advance To Next Simulation
                continue

            # Write Pandas DataFrame To CSV File Within New Directory

            # Provide Some Feedback

            # Advance To Next Ticker
            continue

        # Provide Some Feedback

        # Done; Experiment Complete!
        return

    """
    Write Results (Pandas DataFrame) To CSV File Within Defined Subdirectory
    """
    def save_results(self, directory_path):
        pass






