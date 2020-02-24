"""
WHAT DOES THIS FILE DO


- lists do not need to be copied it is extremely inefficient
"""

import random


def evaluate_individuals(individuals, elite_count):

    # rank individuals by fitness
    ranked_individuals = rank_individuals(individuals)

    # select elites
    elites = ranked_individuals[:elite_count]
    for elite in elites:
        elite.is_elite = True
        elite.lifespan += 1

    # select parents
    parents = select_parents_roulette_rank(ranked_individuals)

    # Return elites, parents
    return elites, parents


def rank_individuals(unranked_individuals):
    n = len(unranked_individuals)

    # rank individuals using quick sort
    ranked_individuals = unranked_individuals.copy()
    quick_sort(ranked_individuals, 0, n-1)

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


# This function takes last element as pivot, places
# the pivot element at its correct position in sorted
# array, and places all smaller (smaller than pivot)
# to left of pivot and all greater elements to right
# of pivot
def partition(arr, low, high):
    i = (low - 1)  # index of smaller element
    pivot = arr[high].fitness()  # pivot

    for j in range(low, high):

        # If current element is smaller than or
        # equal to pivot
        if arr[j].fitness() <= pivot:
            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index

# Function to do Quick sort
def quick_sort(arr, low, high):
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)

        # Separately sort elements before
        # partition and after partition
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)




