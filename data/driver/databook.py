"""

Title : databook.py
Author : Magnus Fyhr
Created : 1/2/2020

Purpose : ...

Development :
    - init                          : DONE
    - launch                        : DONE
    - step                          :
    - close                         : DONE

Testing :
    - init                          :
    - launch                        :
    - step                          :
    - close                         :

"""

from data.driver.helper import purifier

import pandas as pd


class DataBook:

    ticker = ""
    live = False
    book = None

    def __init__(self, ticker):
        self.ticker = ticker
        self.launch()

    def launch(self):
        # load the book
        book = get_databook(self.ticker)

        # verify book is valid
        if verify_databook(book):
            self.live = True
            self.book = book

        # return
        return

    def step(self):
        # sanity check
        if not self.live:
            print("< WRN > : DataBook : Attempted to take a step from a non-live state.")
            return None

        # check if there is another step in the data
        if self.book.shape[0] == 0:
            print("< WRN > : DataBook : Attempted to take a step with no steps remaining.")
            return None

        # take a step, get frame in data and remove it from the book
        frame = self.book[0]
        self.book = self.book.drop[0]

        # convert frame into a dictionary **************

        # return frame of data
        return frame

    def close(self):
        self.live = False
        self.book = None


def get_databook(ticker):
    # obtain pure data frame; either from existing pure or raw csv files
    book_pd_df = purifier.purify_csv(ticker)

    # return data frame
    return book_pd_df


def verify_databook(book):
    # basic verification; object is a pandas data frame
    if not isinstance(book, pd.DataFrame):
        # special debug report ***********
        return False

    # check that columns are present and order matches default
    column_ids = book.columns.values.tolist()
    pure_column_ids = purifier.get_pure_columns()
    if len(column_ids) != len(pure_column_ids):
        # special debug report ***********
        return False
    for i in range(len(column_ids)):
        if column_ids[i] != pure_column_ids[i]:
            # special debug report ***********
            return False

    # otherwise, the book is valid and verified
    return True
