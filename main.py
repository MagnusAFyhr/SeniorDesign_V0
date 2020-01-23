"""

title : main.py
author : Magnus Fyhr
created : 11/22/2019

purpose :

"""

from test import allele_test as ale_tst
from test import chromosome_test as chr_tst
from test import account_test as acc_tst
from test import individual_test as ind_tst
from test import population_test as pop_tst
from test import databook_test as data_tst
from test import habitat_test as hbt_tst

import simulation.habitat.habitat as habi


def run_basic_tests():

    # test allele integrity
    ale_tst.test_allele()

    # test chromosome integrity
    chr_tst.test_chromosome()

    # test account integrity
    acc_tst.test_account()

    # test individual integrity
    ind_tst.test_individual()

    # test population integrity
    pop_tst.test_population()

    # test databook integrity
    data_tst.test_databook()

    # test habitat integrity
    hbt_tst.test_habitat()

    return


def run_advanced_tests():

    # test population diversity

    pass


def run_simulation(ticker):

    habitat = habi.Habitat(ticker)

    i = 0
    while i < 40:
        gen_stats = habitat.simulate_generation()
        habitat.plot(gen_stats)

    pass


# ale_tst.test_allele()

run_simulation("MSFT")
