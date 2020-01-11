"""
WHAT DOES THIS FILE DO
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
        "std": None
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

    # load json object
    json_stats["pop_size"] = pop_size
    json_stats["pop_data"] = pop_fit_data
    json_stats["sum"] = sum_fit
    json_stats["best"] = best_fit
    json_stats["worst"] = worst_fit
    json_stats["mean"] = mean_fit
    json_stats["std"] = std

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

