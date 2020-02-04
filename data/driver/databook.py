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
    - trim_databook                 : DONE

Testing :
    - init                          :
    - launch                        :
    - step                          :
    - close                         :
    - get_databook                  :
    - verify_databook               :
    - trim_databook                 :

TO-DO :
    - Ability to specify range of data or days of simulation to be grabbed
    - Gen_period should also be incorporated, doesn't make sense to have odd amounts

    - Add technical indicators, currently none


"""

from data.driver.helper import purifier

import pandas as pd


class DataBook:

    initialized = False
    _debug_mode = False

    ticker = ""
    live = False
    book = None
    steps = 0

    def __init__(self, ticker, gen_period, days_of_sim=None, start_date=None, end_date=None):

        self.ticker = ticker
        self.launch(gen_period, days_of_sim, start_date, end_date)

    def launch(self, gen_period, days_of_sim, start_date, end_date):
        # load the book
        book = get_databook(self.ticker)

        # trim databook to specified requirements
        book = trim_databook(book, gen_period, days_of_sim, start_date, end_date)

        # verify book is valid
        if verify_databook(book):
            self.live = True
            self.book = book

        # Done Initializing
        self.initialized = True
        return

    def step(self):
        # sanity check
        if not self.live:
            print("< WRN > : DataBook : Attempted to take a step from a non-live state.")
            return None

        # take a step, get frame in data and remove it from the book
        try:
            frame = self.book.iloc[self.steps]
            self.steps += 1
        except IndexError:
            # end of data reached
            print("< WRN > : DataBook : Attempted to take a step with no steps remaining.")
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


def trim_databook(book, gen_period, days_of_sim, start_date, end_date):
    # define trim type to invalid value; so we can recognize if its changed
    trim_type = "INVALID"

    # determine trim type
    if days_of_sim is None and start_date is None and end_date is None:
        pass
    elif days_of_sim is None:
        if start_date is not None and end_date is not None:
            pass  # trim from start_date to end_date
        elif start_date is None and end_date is not None:
            pass  # trim everything past end_date
        elif start_date is not None and end_date is None:
            pass  # trim everything before start_date
    elif days_of_sim is not None:
        if start_date is None and end_date is None:
            pass  # trim everything outside the N most recent days
        elif start_date is None and end_date is not None:
            pass  # trim everything past end_date, and everything before N days before end_date
        elif start_date is not None and end_date is None:
            pass  # trim everything before start_date, and everything after N days after start_date
        elif start_date is not None and end_date is not None:
            pass  # invalid input, all cannot be non-None

    # perform trim according to trim type

    # trim to be evenly divisible by gen_period

    return book

