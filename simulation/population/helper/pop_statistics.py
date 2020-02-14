"""

Title : pop_statistics.py
Author : Magnus Fyhr
Created : 1/7/2020

Purpose :

Development :


Testing :


TO-DO:
    - add account statistics

    - use Simpson diversity index to calculate diversity of technical indicators
        + allele pool technical indicator diversity
            * have used and unused
            * obtain Simpson diversity index of population allele pool
        + chromosome' allele diversity
            * average the Simpson diversity index of all chromosome allele sets

    - change 'stats_dict' to be hierarchical
        + general
            * pop_size
            * best_fit
            * mean_fit
            * worst_fit
            * stdev_fit
            * allele_sdi
            * chrom_sdi
        + performance
            + champion
            + overall

"""


def population_statistics(population):

    # rank the population
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

    # get allele and chromosome diversities
    allele_diversity, chromosome_diversity = population_diversity(population)

    # create dictionary object
    stats_dict = dict([])
    stats_dict["pop_size"] = pop_size
    # stats_dict["pop_data"] = pop_fit_data
    stats_dict["sum_fit"] = sum_fit
    stats_dict["best_fit"] = best_fit
    stats_dict["worst_fit"] = worst_fit
    stats_dict["mean_fit"] = mean_fit
    stats_dict["fit_stdev"] = std
    stats_dict["allele_sdi"] = allele_diversity
    stats_dict["chrom_sdi"] = chromosome_diversity

    return stats_dict


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

    # create data sets
    allele_distributions = dict()
    allele_set_distributions = list([])
    for citizen in population:
        # create dictionary for allele set
        set_dict = dict([])

        allele_set = citizen.chromosome.alleles

        # populate dictionaries
        for allele in allele_set:
            # populate alleles list
            if allele.tech_ind in allele_set:
                allele_distributions[allele.tech_ind] += 1
            else:
                allele_distributions[allele.tech_ind] = 1

            # populate set dictionary
            if allele.tech_ind in set_dict:
                set_dict[allele.tech_ind] += 1
            else:
                set_dict[allele.tech_ind] = 1

        # populate allele sets list with set dictionary
        allele_set_distributions.append(set_dict)

    # allele pool diversity (Simpson's Diversity Index)
    numerator = 0
    total_alleles = 0
    for _, value in allele_distributions.items():
        numerator += value * (value - 1)
        total_alleles += value
    denominator = total_alleles * (total_alleles - 1)
    allele_pool_sdi = 1 - (numerator / denominator)

    # chromosome internal allele set diversity (Simpson's Diversity Index)
    chromosome_count = len(allele_set_distributions)
    sum_chromosome_sdi = 0
    for allele_set in allele_set_distributions:
        numerator = 0
        total_alleles = 0
        for _, value in allele_set.items():
            numerator += value * (value - 1)
            total_alleles += value
        denominator = total_alleles * (total_alleles - 1)
        chromosome_sdi = 1 - (numerator / denominator)
        sum_chromosome_sdi += chromosome_sdi
    average_chromosome_sdi = sum_chromosome_sdi / chromosome_count

    return allele_pool_sdi, average_chromosome_sdi
