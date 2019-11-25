"""

Title : main.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose :

"""

from test import allele_test as ale_tst
from test import chromosome_test as chrm_tst


def run():

    # Test Allele Integrity
    ale_tst.test_allele()

    # Test Chromosome Integrity
    chrm_tst.test_chromosome()


run()
