"""

Title : allele_test.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : To verify the functionality and consistency of the allele class.

Development :
    - test_allele       : DONE
    - test_init         : DONE
    - test_dehydrate    : DONE
    - test_verify       : DONE
    - test_mutate       : DONE
    - test_crossover    : DONE
    - test_react        : DONE

Testing :
    - test_allele       : DONE
    - test_init         : DONE
    - test_dehydrate    : DONE
    - test_verify       : DONE
    - test_mutate       : DONE
    - test_crossover    : DONE
    - test_react        : DONE

"""

import genetics.allele.allele as ale
import time


def test_allele():

    test_difficulty = 10000

    print()
    print("< TEST > : Testing Allele : Difficulty = {}.".format(test_difficulty))
    print()

    # Test Initialization
    init_test = test_init(test_difficulty)

    # Test Dehydration
    dehydrate_test = test_dehydrate(test_difficulty)

    # Test Mutation
    mutate_test = test_mutate(test_difficulty)

    # Test Crossover
    crossover_test = test_crossover(test_difficulty)

    # Test Reaction
    react_test = test_react(test_difficulty)

    print()
    print("< TEST > : Done.")
    print()

    # Return Boolean Test Result
    test_result = init_test and dehydrate_test and mutate_test and crossover_test and react_test
    return test_result


def test_init(difficulty):
    sum_time = 0

    # Test initialization
    init_test = True
    allele = None
    for i in range(difficulty):
        # Execute Initialization, Log Runtime
        start_t = time.time_ns()
        allele = ale.Allele()
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Initialization
        if not allele.initialized:
            init_test = False
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if init_test:
        print("< PASS > : Allele Initialization : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Allele Initialization.")
        print("<      > : Allele : {}.".format(allele.as_string()))

    # Return Boolean Test Result
    return init_test


def test_dehydrate(difficulty):
    sum_time = 0

    # Test dehydration
    dehydrate_test = True
    fail_type = ""
    allele = None
    dehydrated = ""
    for i in range(difficulty):
        allele = ale.Allele()

        # Execute Dehydration, Log Runtime
        start_t = time.time_ns()
        dehydrated = allele.dehydrate()
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Non-NoneType Response
        if dehydrated is None:
            dehydrate_test = False
            fail_type = "NONE"
            break

        # Verify Encoding Match To Original
        if dehydrated != allele.encoding:
            dehydrate_test = False
            fail_type = "DIFF"
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if dehydrate_test:
        print("< PASS > : Allele Dehydrate : Average {} ns per dehydrate().".format(per))
    else:
        print("< FAIL > : Allele Dehydrate      : {}.".format(fail_type))
        print("<      > : Allele                : {}.".format(allele.as_string()))
        print("<      > : Allele Encoding       : {}.".format(allele.encoding))
        print("<      > : Dehydrated Encoding   : {}.".format(dehydrated))

    # Return Boolean Test Result
    return dehydrate_test


def test_mutate(difficulty):
    sum_time = 0

    # Test mutation
    mutate_test = True
    allele = ale.Allele()
    for i in range(difficulty):

        # Execute Mutation, Log Runtime
        start_t = time.time_ns()
        if allele.mutate() is None:
            mutate_test = False
            break
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if mutate_test:
        print("< PASS > : Allele Mutate : Average {} ns per mutate().".format(per))
    else:
        print("< FAIL > : Allele Mutate.")
        print("<      > : Allele                : {}.".format(allele.as_string()))
        print("<      > : Allele Encoding       : {}.".format(allele.encoding))

    return mutate_test


def test_crossover(difficulty):
    sum_time = 0

    # Test Crossover
    crossover_test = True
    allele_a = ale.Allele()
    allele_b = ale.Allele()
    for i in range(difficulty):
        if allele_a is None or allele_b is None:
            crossover_test = False
            break

        # Execute Dehydration, Log Runtime
        start_t = time.time_ns()
        allele_pair = allele_a.crossover(allele_b)
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # update children to be new parents
        allele_a = ale.Allele(allele_pair[0])
        allele_b = ale.Allele(allele_pair[1])

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if crossover_test:
        print("< PASS > : Allele Crossover : Average {} ns per crossover().".format(per))
    else:
        print("< FAIL > : Allele Crossover.")

    # Return Boolean Test Result
    return crossover_test


def test_react(difficulty):
    sum_time = 0

    # Test Reaction
    react_test = True
    fail_type = ""
    allele = ale.Allele()
    for i in range(difficulty):
        # Execute Reaction, Log Runtime
        start_t = time.time_ns()
        low_reaction = allele.react(allele.threshold - 1)
        high_reaction = allele.react(allele.threshold + 1)
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed / 2

        # Verify Non-NoneType Response
        if low_reaction is None or high_reaction is None:
            react_test = False
            fail_type = "NONE"
            break

        # Verify Integer Response
        try:
            int(low_reaction)
            int(high_reaction)

        except ValueError:
            react_test = False
            fail_type = "NOTINT"
            break

        # Verify Threshold Response
        if (low_reaction == 0 and high_reaction == 0) or (low_reaction > 0 and high_reaction > 0):
            react_test = False
            fail_type = "DUAL"
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if react_test:
        print("< PASS > : Allele Reaction : Average {} ns per react().".format(per))
    else:
        print("< FAIL > : Allele Reaction : {}.".format(fail_type))

    # Return Boolean Test Result
    return react_test
