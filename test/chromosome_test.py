"""

Title : chromosome_test.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : To verify the functionality and consistency of the chromosome class.

Development :
    - test_chromosome   : DONE
    - init_test         : DONE
    - dehydrate_test    : DONE
    - verify_test       : DONE
    - mutate_test       : DONE
    - crossover_test    : DONE
    - react_test        : DONE

Testing :
    - test_chromosome   :
    - init_test         :
    - dehydrate_test    :
    - verify_test       :
    - mutate_test       :
    - crossover_test    :
    - react_test        :

"""

import genetics.chromosome.chromosome as chrm
import time


def test_chromosome():

    test_difficulty = 10000

    print()
    print("< TEST > : Testing Chromosome : Difficulty = {}.".format(test_difficulty))
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

    # Test Initialization
    init_test = True
    chromosome = None
    for i in range(difficulty):
        # Execute Dehydration, Log Runtime
        start_t = time.time_ns()
        chromosome = chrm.Chromosome()
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Initialization
        if not chromosome.initialized:
            init_test = False
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if init_test:
        print("< PASS > : Chromosome Initialization : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Chromosome Initialization.")
        print("<      > : Chromosome : {}.".format(chromosome.as_string()))

    # Return Boolean Test Result
    return init_test


def test_dehydrate(difficulty):
    sum_time = 0

    # Test dehydration
    dehydrate_test = True
    fail_type = ""
    chromosome = None
    dehydrated = ""
    for i in range(difficulty):
        chromosome = chrm.Chromosome()

        # Execute Dehydration, Log Runtime
        start_t = time.time_ns()
        dehydrated = chromosome.dehydrate()
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Non-NoneType Response
        if dehydrated is None:
            dehydrate_test = False
            fail_type = "NONE"
            break

        # Verify Encoding Match To Original
        if dehydrated != chromosome.encoding:
            dehydrate_test = False
            fail_type = "DIFF"
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if dehydrate_test:
        print("< PASS > : Chromosome Dehydrate : Average {} ns per dehydrate().".format(per))
    else:
        print("< FAIL > : Chromosome Dehydrate      : {}.".format(fail_type))
        print("<      > : Chromosome                : {}.".format(chromosome.as_string()))
        print("<      > : Chromosome Encoding       : {}.".format(chromosome.encoding))
        print("<      > : Dehydrated Encoding   : {}.".format(dehydrated))

    # Return Boolean Test Result
    return dehydrate_test


def test_mutate(difficulty):
    sum_time = 0

    # Test mutation
    mutate_test = True
    chromosome = chrm.Chromosome()
    for i in range(difficulty):

        # Execute Mutation, Log Runtime
        start_t = time.time_ns()
        if chromosome.mutate() is None:
            mutate_test = False
            break
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if mutate_test:
        print("< PASS > : Chromosome Mutate : Average {} ns per mutate().".format(per))
    else:
        print("< FAIL > : Chromosome Mutate.")
        print("<      > : Chromosome                : {}.".format(chromosome.as_string()))
        print("<      > : Chromosome Encoding       : {}.".format(chromosome.encoding))

    return mutate_test


def test_crossover(difficulty):
    sum_time = 0

    # Test Crossover
    crossover_test = True
    chromosome_a = chrm.Chromosome()
    chromosome_b = chrm.Chromosome()
    for i in range(difficulty):
        if chromosome_a is None or chromosome_b is None:
            crossover_test = False
            break

        # Execute Dehydration, Log Runtime
        start_t = time.time_ns()
        chromosome_pair = chromosome_a.crossover(chromosome_b)
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # update children to be new parents
        chromosome_a = chrm.Chromosome(chromosome_pair[0])
        chromosome_b = chrm.Chromosome(chromosome_pair[1])

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if crossover_test:
        print("< PASS > : Chromosome Crossover : Average {} ns per crossover().".format(per))
    else:
        print("< FAIL > : Chromosome Crossover.")

    # Return Boolean Test Result
    return crossover_test


def test_react(difficulty):
    sum_time = 0

    # Make Dummy Data Dictionary
    dummy_data = {
        '1': 1,  # 1
        '2': 2,  # 2
        '3': 3,  # 3
        '4': 4,  # 4
        '5': 5,  # 5
        '6': 6,  # 6
        '7': 7,  # 7
        '8': 8,  # 8
        '9': 9,  # 9
        '10': 10,  # 10
        '11': 11,  # 11
        '12': 12,  # 12
        '13': 13,  # 13
        '14': 14,  # 14
        '15': 15,  # 15
        '16': 16,  # 16
        '17': 17,  # 17
        '18': 18,  # 18
        '19': 19,  # 19
        '20': 20,  # 20
        '21': 21,  # 21
        '22': 22,  # 22
        '23': 23,  # 23
        '24': 24,  # 24
        '25': 25,  # 25
        '26': 26,  # 26
        '27': 27,  # 27
        '28': 28,  # 28
        '29': 29,  # 29
        '30': 30,  # 30
        '31': 31,  # 31
        '32': 32,  # 32
        '33': 33,  # 33
        '34': 34,  # 34
        '35': 35,  # 35
        '36': 36,  # 36
        '37': 37,  # 37
        '38': 38,  # 38
        '39': 39,  # 39
        '40': 40,  # 40
        '41': 41,  # 41
        '42': 42,  # 42
        '43': 43,  # 43
        '44': 44,  # 44
        '45': 45,  # 45
        '46': 46,  # 46
        '47': 47,  # 47
        '48': 48,  # 48
        '49': 49,  # 49
        '50': 50,  # 50
        '51': 51,  # 51
        '52': 52,  # 52
        '53': 53,  # 53
        '54': 54,  # 54
        '55': 55,  # 55
        '56': 56,  # 56
        '57': 57,  # 57
        '58': 58,  # 58
        '59': 59,  # 59
        '60': 60,  # 60
        '61': 61,  # 61
        '62': 62,  # 62
        '63': 63,  # 63
        '64': 64,  # 64
        '65': 65,  # 65
        '66': 66,  # 66
        '67': 67,  # 67
    }

    # Test Reaction
    react_test = True
    fail_type = ""
    chromosome = chrm.Chromosome()
    for i in range(difficulty):
        # Execute Reaction, Log Runtime
        start_t = time.time_ns()
        reaction = chromosome.react(dummy_data)
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Non-NoneType Response
        if reaction is None:
            react_test = False
            fail_type = "NONE"
            break

        # Verify Response Content
        if reaction != "BUY" and reaction != "SELL" and reaction != "HOLD":
            react_test = False
            fail_type = "INVALID:" + reaction
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if react_test:
        print("< PASS > : Chromosome Reaction : Average {} ns per react().".format(per))
    else:
        print("< FAIL > : Chromosome Reaction : {}.".format(fail_type))

    # Return Boolean Test Result
    return react_test
