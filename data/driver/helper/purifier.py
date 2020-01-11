from pathlib import Path
import pandas as pd
import numpy as np
import data.driver.helper.calculator as ti_calc

raw_columns = ['Date',
               'Open',
               'High',
               'Low',
               'Close',
               'Adj Close',
               'Volume']

pure_columns = ['Date',
                'Open',
                'High',
                'Low',
                'Close',
                'Adj Close',
                'Volume']


def get_pure_databook(ticker):

    # check if ticker has an existing 'pure' type
    # if so, return the already existing csv as a pandas 'DataFrame'
    if pure_dataset_exists(ticker):
        pure_df = pd.read_csv("data/pure/pure_{}.csv".format(ticker))
        return pure_df

    # otherwise, check if ticker has an available 'raw' type
    # if so, create a pure csv from the raw csv
    # then return the pandas 'DataFrame' of the pure csv
    if raw_dataset_exists(ticker):
        raw_df = pd.read_csv("data/raw/{}.csv".format(ticker))
        pure_df = build_pure_csv(raw_df)

        return pure_df

    # sanity check; return None
    print("< ERR > : DataBook : Failed to find historical data for \"{}\".".format(ticker))
    return None


def build_pure_csv(raw_df):
    # initialize pure dataframe
    pure_df = pd.DataFrame(columns=pure_columns)
    pure_df.fillna(0)

    # for each row of raw data...
    for index, _ in raw_df.iterrows():
        # print(raw_row)
        pure_row = ti_calc.build_pure_row(index, raw_df)
        pure_df.loc[index] = pure_row
        if index > 10:
            break

    # for each row of pure data...
    for index, pure_row in pure_df.iterrows():
        print(pure_row)

    # verify pure dataframe
    # write new pure dataframe to pure csv in pure directory

    return raw_df


def pure_dataset_exists(ticker):
    # check if file exists in pure directory
    ticker_file = Path("data/pure/pure_{}.csv".format(ticker))
    if ticker_file.is_file():
        return True

    # otherwise, return false
    return False


def raw_dataset_exists(ticker):
    # check if file exists in raw directory
    ticker_file = Path("data/raw/{}.csv".format(ticker))
    if ticker_file.is_file():
        return True

    # otherwise, return false
    return False


def get_raw_columns():
    return raw_columns.copy()


def get_pure_columns():
    return pure_columns.copy()
