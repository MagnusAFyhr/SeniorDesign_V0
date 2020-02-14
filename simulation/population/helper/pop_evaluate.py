"""
WHAT DOES THIS FILE DO
"""

import random


def evaluate_individuals(individuals, elite_count):

    # rank individuals by fitness
    ranked_individuals = rank_individuals(individuals)

    # select elites
    elites = ranked_individuals[:elite_count]

    # select parents
    parents = select_parents_roulette_rank(ranked_individuals)

    # Return elites, parents
    return elites, parents


def rank_individuals(unranked_individuals):
    n = len(unranked_individuals)
    ranked_individuals = unranked_individuals.copy()

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # traverse the array from 0 to n-i-1
            # Swap if the individual's found fitness
            # is lesser than the next element
            if ranked_individuals[j].fitness() < ranked_individuals[j + 1].fitness():
                temp = ranked_individuals[j]
                ranked_individuals[j] = ranked_individuals[j+1]
                ranked_individuals[j+1] = temp

    # Return ranked individuals
    return ranked_individuals


def select_parents_roulette_rank(pool):
    pool_size = len(pool)
    parents = list([])

    # calculate sum rank
    sum_rank = 0
    for i in range(0, pool_size):
        sum_rank += i

    # select parents
    for i in range(0, pool_size):
        # select random number [0:sum_rank]
        rand_num = random.randint(0, sum_rank)

        # select a new parent; spin roulette wheel
        for j in range(0, rand_num + 1):
            rand_num -= pool_size - j

            if rand_num <= 0:
                # get parent
                parent = pool[j]
                # append to parents
                parents.append(parent)
                # break out of selection
                break

    # return parents
    return parents





