

import pandas


class DataBook:
    def __init__(self, ticker, depth):
        self.live = False
        self.book = []
        self.launch()

    def launch(self):
        self.live = True

    def step(self):
        if not self.live:
            return

    def close(self):
        self.live = False
