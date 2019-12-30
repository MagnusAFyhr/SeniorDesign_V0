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
