"""

Title : databook.py
Author : Magnus Fyhr
Created : 1/2/2020

Purpose : ...

Development :
    - init                          : DONE
    - launch                        : DONE
    - step                          : DONE
    - report                        :
    - status                        :
    - get_databook                  : DONE
    - verify_databook               : DONE
    - trim_databook                 : DONE

Testing :
    - init                          :
    - launch                        :
    - step                          :
    - report                        :
    - status                        :
    - get_databook                  :
    - verify_databook               :
    - trim_databook                 :

Cleaning :
    - init                          : DONE
    - launch                        : DONE
    - step                          : DONE
    - report                        :
    - status                        :
    - get_databook                  :
    - verify_databook               :
    - trim_databook                 :


TO-DO :
    - Add report() function
    - Add status() function

COMMENTS :
    - quick implementation of global variable "AVAIL_TECH_IND"; implementation could be improved

"""

from data.driver.helper import purifier
from analysis import parameters as params

import pandas as pd


class DataBook:

    """
    Initialize DataBook
    """
    def __init__(self, ticker, gen_period, gen_count=None, debug=0):

        # Pre-Initialization
        self.initialized = False
        self._debug_mode = 0
        self._is_debug = False

        self.ticker = ""
        self.live = False
        self.book = None
        self.tech_ind_dict = None
        self.steps = 0

        self.start_date = None
        self.end_date = None

        # Setup Debug Mode
        self._debug_mode = debug
        if self._debug_mode in params.DATABOOK_DEBUG:
            self._is_debug = True

        # Assign & Verify Ticker
        self.ticker = ticker
        if self.ticker not in params.SUPP_TICKERS:
            print("< ERR > : DataBook : Failed to initialize DataBook; '{}' is not a supported ticker!".format(
                self.ticker
            ))
            return

        # Launch DataBook
        self.launch(gen_period, gen_count)

        # Verify DataBook
        if not self.live:
            print("< ERR > : DataBook : Failed to initialize DataBook; launch failed.")
            return

        # Print DataBook Characteristics To Console
        if self._debug_mode in params.DATABOOK_CONSOLE:
            pass

        # Initialization Complete!
        self.initialized = True
        return

    """
    Obtain Historical Data For DataBook
    """
    def launch(self, gen_period, gen_count):

        # Soft Reset
        self.live = False
        self.book = None
        self.steps = 0

        # Obtain The Historical Data
        book = get_databook(self.ticker)

        # Trim Historical Data To Specified Requirements
        book = trim_databook(book, gen_period, gen_count)

        # Verify Historical Data
        if verify_databook(book):
            self.live = True
            self.book = book
            self.start_date = self.book.iloc[0, 0]
            self.end_date = self.book.iloc[len(book.index) - 1, 0]

        # Create Encoding Dictionary For Alleles; Update Global Variables
        ti_dict = dict()
        i = 0
        for ti in self.book.columns.values.tolist():
            if ti == "Date":
                continue
            key = chr(i + 48)
            value = ti
            ti_dict[key] = value
            i += 1
        self.tech_ind_dict = ti_dict

        # Launch Complete!
        return

    """
    Take A Step In The Historical Data; Obtain The Subsequent Frame Of Data
    """
    def step(self):

        # Sanity Check
        if not self.live:
            print("< ERR > : DataBook : Attempted to take a step from a non-live state.")
            return None

        # Take A Step; Obtain Subsequent Frame In Data
        try:
            frame = self.book.iloc[self.steps]
            self.steps += 1
        except IndexError:
            # end of data reached
            print("< ERR > : DataBook : Attempted to take a step with no steps remaining.")
            return "EOF"

        # Convert Frame Into A Dictionary Object
        data_dict = frame.to_dict()

        # Verify Data Dictionary; Single Row Of Pandas Data
        if self._is_debug:
            pass

        # Step Complete; Return Frame Of Data
        return data_dict

    """
    Print DataBook Characteristics To Debug Console
    """
    def report(self):
        pass

    """
    Returns Dictionary Representation Of DataBook's Characteristics
    """
    def status(self):
        pass


def get_databook(ticker):
    """ Obtain Historical Data Of Specified Ticker As Pandas DataFrame """

    # Obtain Pandas Data Frame
    book_pd_df = purifier.get_pure_databook(ticker)

    # Return Pandas Data Frame
    return book_pd_df


def verify_databook(book):
    """ Verify Historical Data For DataBook """

    # basic verification; object is a pandas data frame
    if not isinstance(book, pd.DataFrame):
        print("< ERR > : DataBook : Failed to verify DataBook; result not of type 'DataBook'.")
        return False

    # check that columns are present and order matches default
    column_ids = book.columns.values.tolist()
    dict_columns = {i: True for i in column_ids}

    #pure_column_ids = purifier.get_pure_columns()
    #for i in range(len(pure_column_ids)):
    #    if dict_columns[pure_column_ids[i]] is None:
    #        print("< ERR > : DataBook : Failed to find column data for {}.".format(pure_column_ids[i]))
    #        return False

    # Verification Complete!
    return True


def trim_databook(book, gen_period, gen_count):
    """ Trim Historical Data To Specified Requirements For DataBook """

    # apply trim
    if gen_count is None:
        pass
    else:
        if gen_count * gen_period < len(book.index):
            book = book.iloc[len(book.index) - (gen_count * gen_period) - 1:]

    # trim to be evenly divisible by gen_period
    excess = len(book.index) % gen_period
    book = book.iloc[excess:]

    return book

