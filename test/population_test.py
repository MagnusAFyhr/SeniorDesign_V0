"""

Title : population_test.py
Author : Magnus Fyhr
Created : 12/18/2019

Purpose : To verify the functionality and consistency of the population class.

Development :
    - test_population       :
    - init_test             : DONE
    - step_test             : DONE
    - evaluate_test         : DONE
    - reproduce_test        : DONE
    - modify_test           :
    - next_generation_test  :
    - metrics_test          :

Testing :
    - test_population       :
    - init_test             :
    - step_test             :
    - next_generation_test  :
    - evaluate_test         :
    - reproduce_test        :
    - modify_test           :
    - statistics_test       :

"""

from simulation.population import population as popu

import time
import random
from datetime import datetime

pop_test_size = 100
pop_test_iters = 50

def test_population():

    test_difficulty = 1000

    print()
    print("< TEST > : Testing Population : Difficulty = {}.".format(test_difficulty))
    print()

    init_test = test_init(test_difficulty)

    step_test = test_step(test_difficulty)

    evaluation_test = test_evaluate(test_difficulty)

    reproduction_test = test_reproduce(test_difficulty)

    modification_test = test_modify(test_difficulty)

    metrics_test = test_metrics(test_difficulty)

    next_gen_test = test_next_generation(test_difficulty)

    print()
    print("< TEST > : Done.")
    print()

    # Return Boolean Test Result
    test_result = init_test and step_test\
        and evaluation_test and reproduction_test and modification_test\
        and metrics_test and next_gen_test
    return test_result


def test_init(difficulty):
    sum_time = 0

    # Test Random Initialization
    init_test = True
    fail_data = ""
    for i in range(difficulty):
        if not init_test:
            break

        # Execute Initialization, Log Runtime
        start_t = time.time_ns()

        population = popu.Population(pop_test_size)

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify population
        fail_data = population.size
        if len(population.citizens) != population.size:
            init_test = False
        for individual in population.citizens:
            if not individual.initialized:
                init_test = False

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if init_test:
        print("< PASS > : Population Initialization : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Population Initialization.")
        print("<      > : Pop. Size : {}.".format(fail_data))

    # Return Boolean Test Result
    return init_test


def test_step(difficulty):
    sum_time = 0

    population = popu.Population(difficulty)

    # Test Step
    step_test = True
    for i in range(difficulty):
        if not step_test:
            break

        observation = random_observation()

        # Execute Initialization, Log Runtime
        start_t = time.time_ns()

        population.step(observation)

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Step
        if population.step_count != i:
            step_test = False
        if population.iter_count != difficulty * i:
            step_test = False

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if step_test:
        print("< PASS > : Population Step : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Population Step.")
        print("<      > : Step Count : {}.".format(population.step_count))
        print("<      > : Iter Count : {}.".format(population.iter_count))

    # Return Boolean Test Result
    return step_test


def test_evaluate(difficulty):
    sum_time = 0

    # Test Evaluate
    evaluate_test = True
    fail_type = "NULL"
    fail_data = "NULL"
    for i in range(difficulty):
        if not evaluate_test:
            break

        # Create random population
        population = popu.Population(pop_test_size)
        # Simulate random test case
        population = simulate_steps(population, 50)

        # Execute Evaluation, Log Runtime
        start_t = time.time_ns()

        elites, parents = population.evaluate()

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Evaluation
        if len(elites) <= 0 or len(parents) <= 0:
            evaluate_test = False
            fail_type = "SIZE"
            fail_data = [len(elites), len(parents)]
        for elite in elites:
            if not elite.verify():
                evaluate_test = False
                fail_type = "BAD_ELITE"
                fail_data = ""
        for parent in parents:
            if not parent.verify():
                evaluate_test = False
                fail_type = "BAD_PARENT"
                fail_data = ""

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if evaluate_test:
        print("< PASS > : Population Evaluation : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Population Evaluation     : {}.".format(fail_type))
        if fail_type == "SIZE":
            print("<      > : (Elites, Parents) : ({}).".format(fail_data))
        if fail_type == "BAD_ELITE" or fail_type == "BAD_PARENT":
            pass

    # Return Boolean Test Result
    return evaluate_test


def test_reproduce(difficulty):
    sum_time = 0

    # Create random population
    population = popu.Population(difficulty)
    # Simulate random test case
    population = simulate_steps(population, 50)
    # Evaluate population
    elites, parents = population.evaluate()

    # Test Reproduce
    reproduce_test = True
    fail_type = "NULL"
    fail_data = ""
    for i in range(difficulty):
        if not reproduce_test:
            break

        # Execute Reproduction, Log Runtime
        start_t = time.time_ns()

        offspring = population.reproduce(parents)

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Reproduction
        if len(offspring) != len(parents) * 2:
            reproduce_test = False
            fail_type = "SIZE"
            fail_data = [len(parents), len(offspring)]
        for chromosome in offspring:
            if not chromosome.verify():
                reproduce_test = False
                fail_type = "BAD_CHILD"

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if reproduce_test:
        print("< PASS > : Population Reproduction : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Population Reproduction       : {}.".format(fail_type))
        if fail_type == "SIZE":
            print("<      > : (Parents, Children) : ({}).".format(fail_data))
        if fail_type == "BAD_CHILD":
            pass

    # Return Boolean Test Result
    return reproduce_test


def test_modify(difficulty):
    sum_time = 0

    # Create random population
    population = popu.Population(difficulty)
    # Simulate random test case
    population = simulate_steps(population, 50)
    # Evaluate population
    elites, parents = population.evaluate()
    # Reproduce population
    offspring = population.reproduce(parents)

    # Test Modify
    modify_test = True
    fail_type = "NULL"
    fail_data = ""
    for i in range(difficulty):
        if not modify_test:
            break

        # Execute Modification, Log Runtime
        start_t = time.time_ns()

        offspring = population.modify(offspring)

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Modification
        if len(offspring) != len(parents) * 2:
            modify_test = False
            fail_type = "SIZE"
            fail_data = [len(parents), len(offspring)]
        for chromosome in offspring:
            if not chromosome.verify():
                modify_test = False
                fail_type = "BAD_CHILD"
    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if modify_test:
        print("< PASS > : Population Modification : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Population Modification       : {}.".format(fail_type))
        if fail_type == "SIZE":
            print("<      > : (Children, Modification) : ({}).".format(fail_data))
        if fail_type == "BAD_CHILD":
            pass
    # Return Boolean Test Result
    return modify_test


def test_metrics(difficulty):
    sum_time = 0

    # Test Metrics
    metrics_test = True
    for i in range(difficulty):
        if not metrics_test:
            break

        # Execute Metrics, Log Runtime
        start_t = time.time_ns()

        # PUT TESTING CODE HERE

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Metrics
        # PUT VERIFICATION CODE HERE

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if metrics_test:
        print("< PASS > : Population Modification : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Population Modification.")

    # Return Boolean Test Result
    return metrics_test


def test_next_generation(difficulty):
    sum_time = 0

    # Test Next Generation
    next_gen_test = True
    for i in range(difficulty):
        if not next_gen_test:
            break

        # Execute Generation, Log Runtime
        start_t = time.time_ns()

        # PUT TESTING CODE HERE

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Generation
        # PUT VERIFICATION CODE HERE

    # Calculate Average Runtime
    per = sum_time / difficulty

    # Print Test Result
    if next_gen_test:
        print("< PASS > : Population Modification : Average {} ns per __init__().".format(per))
    else:
        print("< FAIL > : Population Modification.")

    # Return Boolean Test Result
    return next_gen_test


def simulate_steps(population, n_steps):

    # iterate
    for _ in range(n_steps):
        # take random_observation
        observation = random_observation()

        # simulate step within population
        population.step(observation)

    return population


def random_observation():
    rand_data = random.uniform(0, 1000)

    # Make Dummy Data Dictionary
    dummy_data = {
        'TIMESTAMP': datetime.now(),  # Timestamp
        'PRICE': 100.00,  # Price
        '1': rand_data,  # 1
        '2': rand_data,  # 2
        '3': rand_data,  # 3
        '4': rand_data,  # 4
        '5': rand_data,  # 5
        '6': rand_data,  # 6
        '7': rand_data,  # 7
        '8': rand_data,  # 8
        '9': rand_data,  # 9
        '10': rand_data,  # 10
        '11': rand_data,  # 11
        '12': rand_data,  # 12
        '13': rand_data,  # 13
        '14': rand_data,  # 14
        '15': rand_data,  # 15
        '16': rand_data,  # 16
        '17': rand_data,  # 17
        '18': rand_data,  # 18
        '19': rand_data,  # 19
        '20': rand_data,  # 20
        '21': rand_data,  # 21
        '22': rand_data,  # 22
        '23': rand_data,  # 23
        '24': rand_data,  # 24
        '25': rand_data,  # 25
        '26': rand_data,  # 26
        '27': rand_data,  # 27
        '28': rand_data,  # 28
        '29': rand_data,  # 29
        '30': rand_data,  # 30
        '31': rand_data,  # 31
        '32': rand_data,  # 32
        '33': rand_data,  # 33
        '34': rand_data,  # 34
        '35': rand_data,  # 35
        '36': rand_data,  # 36
        '37': rand_data,  # 37
        '38': rand_data,  # 38
        '39': rand_data,  # 39
        '40': rand_data,  # 40
        '41': rand_data,  # 41
        '42': rand_data,  # 42
        '43': rand_data,  # 43
        '44': rand_data,  # 44
        '45': rand_data,  # 45
        '46': rand_data,  # 46
        '47': rand_data,  # 47
        '48': rand_data,  # 48
        '49': rand_data,  # 49
        '50': rand_data,  # 50
        '51': rand_data,  # 51
        '52': rand_data,  # 52
        '53': rand_data,  # 53
        '54': rand_data,  # 54
        '55': rand_data,  # 55
        '56': rand_data,  # 56
        '57': rand_data,  # 57
        '58': rand_data,  # 58
        '59': rand_data,  # 59
        '60': rand_data,  # 60
        '61': rand_data,  # 61
        '62': rand_data,  # 62
        '63': rand_data,  # 63
        '64': rand_data,  # 64
        '65': rand_data,  # 65
        '66': rand_data,  # 66
        '67': rand_data,  # 67
    }

    # Return Random Observation
    return dummy_data
