from pathlib import Path
import pandas as pd
import data.driver.helper.calculator as calc


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
        raw_df = pd.read_csv("data/raw/{}.csv".format(ticker), sep=',')
        pure_df = build_pure_csv(ticker, raw_df)

        return pure_df

    # sanity check; return None
    print("< ERR > : DataBook : Failed to find historical data for \"{}\".".format(ticker))
    return None


def build_pure_csv(ticker, raw_df):
    # build the pure dataframe
    pure_df = calc.build_pure_dataframe(raw_df)

    # write the pure dataframe to a csv in pure directory
    # pure_df.to_csv("data/pure/pure_{}.csv".format(ticker), sep=',')

    return pure_df


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
