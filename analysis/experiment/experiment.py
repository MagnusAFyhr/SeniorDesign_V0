"""

Title : experiment.py
Author : Magnus Fyhr
Created : 02/05/2020

Purpose :


Development :


Testing :


TO-DO:


Comments :


"""


class Experiment(object):

    ticker = ""
    sample_size = 0

    """
    Initialize & Verify The Experiment
    """
    def __init__(self, ticker, sample_size=30):
        self.ticker = ticker
        self.sample_size = sample_size

        return

    def run(self):
        pass




