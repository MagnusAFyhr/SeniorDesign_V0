"""

Title : pop_statistics.py
Author : Magnus Fyhr
Created : 1/7/2020

Purpose :

Development :


Testing :


TO-DO:
    - add account statistics
    - add calculation for standard deviation for diversity : DONE


"""


def population_statistics(population):

    # create json object
    json_stats = {
        "pop_size": None,
        "pop_data": None,
        "sum": None,
        "best": None,
        "worst": None,
        "mean": None,
        "std": None,
        "diversity": None
    }

    population = rank_population(population)

    # get population size
    pop_size = len(population)

    # get population data; list of fitness
    pop_fit_data = [citizen.fitness() for citizen in population]

    # get population sum fitness
    sum_fit = sum(pop_fit_data)

    # get population best fitness
    best_fit = population[0].fitness()

    # get population worst fitness
    worst_fit = population[pop_size - 1].fitness()

    # get population mean fitness
    mean_fit = sum_fit / pop_size

    # get population standard deviation
    std = population_stand_dev(population, mean_fit)

    # get population diversity
    diversity = population_diversity(population)

    # load json object
    json_stats["pop_size"] = pop_size
    json_stats["pop_data"] = pop_fit_data
    json_stats["sum"] = sum_fit
    json_stats["best"] = best_fit
    json_stats["worst"] = worst_fit
    json_stats["mean"] = mean_fit
    json_stats["std"] = std
    json_stats["diversity"] = diversity  # json object

    return json_stats


def population_stand_dev(population, mean_fitness):
    sum_sq_var = 0
    for citizen in population:
        variance = citizen.fitness() - mean_fitness
        sq_var = pow(variance, 2)
        sum_sq_var += sq_var

    variance = sum_sq_var / (len(population) - 1)
    stand_dev = pow(variance, 0.5)

    return stand_dev


def rank_population(population):
    n = len(population)

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if population[j].fitness() < population[j + 1].fitness():
                temp = population[j]
                population[j] = population[j + 1]
                population[j + 1] = temp

    return population


def population_diversity(population):

    # allele pool and distributions
    allele_distribution = dict()
    for citizen in population:
        for allele in citizen.chromosome.alleles:
            if allele.tech_ind in allele_distribution:
                allele_distribution[allele.tech_ind] += 1
            else:
                allele_distribution[allele.tech_ind] = 1

    # high; low; mean; std; distribution percentage
    used_count = 0
    unused_count = 0
    sum_count = 0
    high_count = None
    low_count = None
    for key, value in allele_distribution.items():
        # sum
        sum_count += value

        # high
        if high_count is None:
            high_count = value
        elif high_count < value:
            high_count = value

        # low
        if low_count is None:
            low_count = value
        elif low_count > value:
            low_count = value

        # distribution percentage
        if value == 0:
            unused_count += 1
        else:
            used_count += 1

    # obtain pool size
    pool_size = len(allele_distribution)

    # calculate mean
    mean_count = round(sum_count / pool_size, 2)

    # calculate standard deviation
    sum_sq_var = 0
    for _, value in allele_distribution.items():
        variance = value - mean_count
        sq_var = pow(variance, 2)
        sum_sq_var += sq_var
    variance = sum_sq_var / (pool_size - 1)
    stand_dev = pow(variance, 0.5)

    # calculate distribution percentage
    distribution = round((used_count / pool_size) * 100, 2)

    # make json object (dict)
    json = {
        "used": used_count,
        "unused": unused_count,
        "sum": sum_count,
        "high": high_count,
        "low": low_count,
        "mean": mean_count,
        "std": stand_dev,
        "percent": distribution
    }

    return json
