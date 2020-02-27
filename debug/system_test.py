"""

Title : system_test.py
Author : Magnus Fyhr
Created :

Purpose : ...

Development :
    - test_system           :

Testing :

"""

from debug.components import individual_test as ind_tst, habitat_test as hbt_tst, account_test as acc_tst, \
    population_test as pop_tst, databook_test as data_tst, allele_test as ale_tst, chromosome_test as chr_tst


def test_system():

    test_difficulty = 1

    print()
    print("< TEST > : Testing System : Difficulty = {}.".format(test_difficulty))
    print()

    # Basics
    basic_tests = run_basic_tests()

    # Diversity
    diversity_test = False

    print()
    print("< TEST > : Done.")
    print()

    # Return Boolean Test Result
    test_result = basic_tests and diversity_test
    return test_result


def run_basic_tests():

    # test allele integrity
    allele_test = ale_tst.test_allele()

    # test chromosome integrity
    chromosome_test = chr_tst.test_chromosome()

    # test account integrity
    account_test = acc_tst.test_account()

    # test individual integrity
    individual_test = ind_tst.test_individual()

    # test population integrity
    population_test = pop_tst.test_population()

    # test databook integrity
    databook_test = data_tst.test_databook()

    # test habitat integrity
    habitat_test = hbt_tst.test_habitat()

    return allele_test and chromosome_test and \
        account_test and individual_test and \
        population_test and databook_test and habitat_test

