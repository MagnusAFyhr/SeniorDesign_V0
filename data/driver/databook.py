"""

Title : databook.py
Author : Magnus Fyhr
Created : 1/2/2020

Purpose : ...

Development :
    - init                          : DONE
    - launch                        : DONE
    - step                          : DONE
    - close                         : DONE
    - get_databook                  : DONE
    - verify_databook               : DONE

Testing :
    - init                          :
    - launch                        :
    - step                          :
    - close                         :

TO-DO :
    - Ability to specify range of data to be grabbed
    - Add technical indicators, currently none



"""

from data.driver.helper import purifier

import pandas as pd


class DataBook:

    ticker = ""
    live = False
    book = None

    def __init__(self, ticker):
        self.steps = 0
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
        self.steps += 1
        try:
            frame = self.book.iloc[self.steps]
        except IndexError:
            # end of data reached
            return "EOF"

        # convert frame into a dictionary
        data_dict = frame.to_dict()

        # return frame of data
        return data_dict

    def close(self):
        self.live = False
        self.book = None
        self.steps = 0


def get_databook(ticker):
    # obtain pure data frame; either from existing pure or raw csv files
    book_pd_df = purifier.get_pure_databook(ticker)

    # return data frame
    return book_pd_df


def verify_databook(book):
    # basic verification; object is a pandas data frame
    if not isinstance(book, pd.DataFrame):
        print("< ERR > : DataBook : Extracted data is not of type 'DataBook'.")
        return False

    # check that columns are present and order matches default
    column_ids = book.columns.values.tolist()
    dict_columns = {i: True for i in column_ids}

    pure_column_ids = purifier.get_pure_columns()
    for i in range(len(pure_column_ids)):
        if dict_columns[pure_column_ids[i]] is None:
            print("< WRN > : DataBook : Failed to find column data for {}.".format(pure_column_ids[i]))
            return False

    # otherwise, the book is valid and verified
    return True
