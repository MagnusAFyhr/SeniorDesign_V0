"""

Title : habitat_test.py
Author : Magnus Fyhr
Created : 1/9/2020

Purpose : To verify the functionality and consistency of the population class.

Development :
    - test_habitat          : DONE
    - test_init             : DONE
    - test_simulate         : DONE

Testing :
    - test_habitat          : DONE
    - test_init             : DONE
    - test_simulate         : DONE

"""

import time
import simulation.habitat.habitat as habi


def test_habitat():

    test_difficulty = 10

    print()
    print("< TEST > : Testing Habitat : Difficulty = {}.".format(test_difficulty))
    print()

    init_test = test_init(test_difficulty)

    simulate_test = test_simulate(test_difficulty)

    print()
    print("< TEST > : Done.")
    print()

    # Return Boolean Test Result
    test_result = init_test and simulate_test
    return test_result


def test_init(difficulty):
    sum_time = 0

    # Test Initialization
    init_test = True
    for i in range(difficulty):
        # Execute Initialization, Log Runtime
        start_t = time.time_ns()

        habitat = habi.Habitat("MSFT")

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Initialization
        if not habitat.environment.live and len(habitat.population.citizens) == habitat.population.size:
            init_test = False
            break

    # Calculate Average Runtime
    sum_time /= pow(10, 6)
    per = sum_time / difficulty

    # Print Test Result
    if init_test:
        print("< PASS > : Habitat Initialization : Average {} ms per __init__().".format(per))
    else:
        print("< FAIL > : Habitat Initialization.")

    # Return Boolean Test Result
    return init_test


def test_simulate(difficulty):
    sum_time = 0

    habitat = habi.Habitat("MSFT")

    # Test Simulation
    simulate_test = True
    for i in range(difficulty):
        if not simulate_test:
            break

        # Execute Simulation, Log Runtime
        start_t = time.time_ns()

        gen_stats = habitat.simulate_generation()

        end_t = time.time_ns()
        elapsed = end_t - start_t
        sum_time += elapsed

        # Verify Simulation
        for key, value in gen_stats.items():
            if value is None:
                simulate_test = False
                break

    # Calculate Average Runtime
    sum_time /= pow(10, 9)
    per = sum_time / difficulty

    # Print Test Result
    if simulate_test:
        print("< PASS > : Habitat Generation Simulation : Average {} sec per simulate_generation().".format(per))
    else:
        print("< FAIL > : Habitat Generation Simulation.")

    # Return Boolean Test Result
    return simulate_test

