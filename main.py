"""

Title : main.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose :

"""

from test import allele_test as ale_tst
from test import chromosome_test as chr_tst
from test import account_test as acc_tst
from test import individual_test as ind_tst


def run():

    # Test Allele Integrity
    ale_tst.test_allele()

    # Test Chromosome Integrity
    chr_tst.test_chromosome()

    # Test Account Integrity
    acc_tst.test_account()

    # Test Individual Integrity
    ind_tst.test_individual()

    # Test Data Manager Integrity


run()
