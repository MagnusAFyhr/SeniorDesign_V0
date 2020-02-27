"""
WHAT DOES THIS FILE DO


- lists do not need to be copied it is extremely inefficient
"""

import random


def evaluate_individuals(individuals, elite_count):

    # rank individuals by fitness
    rank_individuals(individuals)

    # select elites
    elites = individuals[:elite_count]
    for elite in elites:
        elite.is_elite = True
        elite.lifespan += 1

    # select parents
    parents = select_parents_roulette_rank(individuals)

    # Return elites, parents
    return elites, parents


def rank_individuals(unranked_individuals):
    n = len(unranked_individuals)

    # rank individuals using iterative quick sort
    quick_sort_iterative(unranked_individuals, 0, n-1)

    # Return ranked individuals
    return unranked_individuals


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
    i = (low - 1)
    pivot = arr[high]

    for j in range(low, high):
        if arr[j].fitness() >= pivot.fitness():
            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Function to do Recursive Quick sort
# arr[] --> Array to be sorted,
# start  --> Starting index,
# end  --> Ending index
def quick_sort_recursive(arr, start, end):
    if start < end:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, start, end)

        # Separately sort elements before
        # partition and after partition
        quick_sort_recursive(arr, start, pi - 1)
        quick_sort_recursive(arr, pi + 1, end)


# Function to do Iterative Quick sort
# arr[] --> Array to be sorted,
# l  --> Starting index,
# h  --> Ending index
def quick_sort_iterative(arr, low, high):
    # Create an auxiliary stack
    size = high - low + 1
    stack = [0] * size

    # initialize top of stack
    top = -1

    # push initial values of low and high to stack
    top = top + 1
    stack[top] = low
    top = top + 1
    stack[top] = high

    # Keep popping from stack while is not empty
    while top >= 0:

        # Pop high and low
        high = stack[top]
        top = top - 1
        low = stack[top]
        top = top - 1

        # Set pivot element at its correct position in
        # sorted array
        p = partition(arr, low, high)

        # If there are elements on left side of pivot,
        # then push left side to stack
        if p - 1 > low:
            top = top + 1
            stack[top] = low
            top = top + 1
            stack[top] = p - 1

        # If there are elements on right side of pivot,
        # then push right side to stack
        if p + 1 < high:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = high
