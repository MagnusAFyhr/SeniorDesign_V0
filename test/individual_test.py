"""

Title : individual_test.py
Author : Magnus Fyhr
Created : 12/1/2019

Purpose : To verify the functionality and consistency of the individual class.

Development :
    - test_individual   : DONE
    - init_test         : DONE
    - step_test         : DONE
    - fitness_test      : DONE
    - mate_test         : DONE
    - clone_test        : DONE

Testing :
    - test_individual   : DONE
    - init_test         : DONE
    - step_test         : DONE
    - fitness_test      : DONE
    - mate_test         : DONE
    - clone_test        : DONE

"""

from genetics.chromosome import chromosome as chrm
from phenetics.individual import individual as indi

import time
import random
from datetime import datetime


def test_individual():

    test_difficulty = 10000

    print()
    print("< TEST > : Testing Individual : Difficulty = {}.".format(test_difficulty))
    print()

    init_test = test_init(test_difficulty)

    step_test = test_step(test_difficulty)

    fitness_test = test_fitness(test_difficulty)

    mate_test = test_mate(test_difficulty)

    clone_test = test_clone(test_difficulty)

    print()
    print("< TEST > : Done.")
    print()

    # Return Boolean Test Result
    test_result = init_test and step_test and fitness_test and mate_test and clone_test
    return test_result


def test_init(difficulty):
    sum_time = 0

    # Half the test is using chromosome to initialize Individual, half is using None
    half = int(difficulty/2)

    # Test Initialization Using Pre-Initialized Chromosome
    init_test = True
    individual = None
    for i in range(half):
        # Execute Initialization, Log Runtime
        start_t = time.time_ns()
        chromosome = chrm.Chromosome()
        individual = indi.Individual(chromosome)
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Initialization
        if not individual.initialized:
            init_test = False
            break

    # Test Random Initialization
    for i in range(half):
        if not init_test:
            break

        # Execute Initialization, Log Runtime
        start_t = time.time_ns()
        individual = indi.Individual()
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Initialization
        if not individual.initialized:
            init_test = False
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if init_test:
        print("< PASS > : Individual Initialization : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Individual Initialization.")
        print("<      > : Individual : {}.".format(individual.as_json()))

    # Return Boolean Test Result
    return init_test


def test_step(difficulty):
    sum_time = 0

    # Create Number Of Steps To Be Executed Per Sample (Iterations = difficulty * step_count)
    step_count = 20

    # Make Dummy Data Dictionary
    dummy_data = {
        'TIMESTAMP': datetime.now(),  # Timestamp
        'PRICE': 100.00,  # Price
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

    # Test Step Function
    step_test = True
    individual = None
    for i in range(difficulty):
        # Create Individual
        individual = indi.Individual()

        # Perform Steps
        for j in range(step_count):
            # Load Random Data Dictionary
            for tech_ind in dummy_data:
                if tech_ind == "TIMESTAMP":
                    dummy_data[tech_ind] = datetime.now()
                elif tech_ind == "PRICE":
                    dummy_data[tech_ind] = dummy_data[tech_ind] + random.uniform(-1, 1)
                else:
                    dummy_data[tech_ind] = random.uniform(0, 1000)

            # Execute Step, Log Runtime
            start_t = time.time_ns()
            feedback = individual.step(dummy_data)
            end_t = time.time_ns()
            elapsed = end_t - start_t
            sum_time += elapsed

            # Verify Step Execution
            if feedback is None:
                step_test = False
                break

    # Calculate Average Runtime
    per = sum_time / (difficulty * step_count)

    # Print Test Result
    if step_test:
        print("< PASS > : Individual Step  : Average {} ns per step().".format(per))
    else:
        print("< FAIL > : Individual Step.")
        print("<      > : Individual : {}.".format(individual.as_json()))

    # Return Boolean Test Result
    return step_test


def test_fitness(difficulty):
    sum_time = 0

    # Test Fitness Function
    fitness_test = True
    for i in range(difficulty):
        # Create Individual
        individual = indi.Individual()

        # Calculate Fitness
        try:
            start_t = time.time_ns()
            individual.fitness()
            end_t = time.time_ns()
            elapsed = end_t - start_t
            sum_time += elapsed
        except ValueError or ZeroDivisionError or ArithmeticError:
            fitness_test = False
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if fitness_test:
        print("< PASS > : Individual Fitness  : Average {} ns per fitness().".format(per))
    else:
        print("< FAIL > : Individual Fitness.")

    # Return Boolean Test Result
    return fitness_test


def test_mate(difficulty):
    sum_time = 0

    # Test Mate Function
    mate_test = True
    fail_type = ""
    individual_a = indi.Individual()
    individual_b = indi.Individual()
    for i in range(difficulty):
        # Mate Individual A with B, Log Runtime
        start_t = time.time_ns()
        offspring_chromosomes = individual_a.mate(individual_b)
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Mate Execution
        if offspring_chromosomes is None:
            mate_test = False
            fail_type = "NONE_OFFSPRING"
            break

        if len(offspring_chromosomes) != 2:
            mate_test = False
            fail_type = "OFFSPRING_SIZE_{}".format(len(offspring_chromosomes))
            break

        # Form New Individuals
        individual_a = indi.Individual(offspring_chromosomes[0])
        individual_b = indi.Individual(offspring_chromosomes[1])

        # Verify Next Initialization
        if not individual_a.initialized or not individual_b.initialized:
            mate_test = False
            fail_type = "BAD_CHROM"
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if mate_test:
        print("< PASS > : Individual Mate  : Average {} ns per mate().".format(per))
    else:
        print("< FAIL > : Individual Mate : {}.".format(fail_type))

    # Return Boolean Test Result
    return mate_test


def test_clone(difficulty):
    sum_time = 0

    # Test Mate Function
    clone_test = True
    fail_type = ""
    individual = indi.Individual()
    for i in range(difficulty):
        # Clone Individual, Log Runtime
        start_t = time.time_ns()
        clone_chromosome = individual.clone()
        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Form New Individual
        individual = indi.Individual(clone_chromosome)

        # Verify Next Initialization
        if not individual.initialized:
            clone_test = False
            fail_type = "BAD_CLONE"
            break

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if clone_test:
        print("< PASS > : Individual Clone  : Average {} ns per clone().".format(per))
    else:
        print("< FAIL > : Individual Clone : {}.".format(fail_type))

    # Return Boolean Test Result
    return clone_test
