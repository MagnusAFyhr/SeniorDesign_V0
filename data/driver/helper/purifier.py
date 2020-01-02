from pathlib import Path
import pandas as pd


raw_columns = ['date',
               'open',
               'high',
               'low',
               'close',
               'adj close',
               'volume']

pure_columns = ['date',
                'open',
                'high',
                'low',
                'close',
                'adj close',
                'volume']


def purify_csv(ticker):
    # check if ticker has an existing 'pure' type
    # if so, return the already existing csv as a pandas 'DataFrame'
    if pure_dataset_exists(ticker):
        pure_df = pd.read_csv("../../pure/pure_{}.csv".format(ticker), delimeter=',')
        return pure_df

    # otherwise, check if ticker has an available 'raw' type
    # if so, create a pure csv from the raw csv
    # then return the pandas 'DataFrame' of the pure csv
    if raw_dataset_exists(ticker):
        raw_df = pd.read_csv("../../raw/{}.csv".format(ticker), delimeter=',')
        pure_df = build_pure_csv(raw_df)
        return pure_df

    # sanity check; return None
    return None


def build_pure_csv(raw_df):
    return list([])


def pure_dataset_exists(ticker):
    # check if file exists in pure directory
    ticker_file = Path("../../pure/pure_{}.csv".format(ticker))
    if ticker_file.is_file():
        return True

    # otherwise, return false
    return False


def raw_dataset_exists(ticker):
    # check if file exists in raw directory
    ticker_file = Path("../../raw/{}.csv".format(ticker))
    if ticker_file.is_file():
        return True

    # otherwise, return false
    return False


def get_raw_columns():
    return raw_columns.copy()


def get_pure_columns():
    return pure_columns.copy()
