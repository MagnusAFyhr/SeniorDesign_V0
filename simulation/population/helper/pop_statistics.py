"""

Title : pop_statistics.py
Author : Magnus Fyhr
Created : 1/7/2020

Purpose :

Development :


Testing :


TO-DO:
    - add account statistics

    - change 'stats_dict' to be hierarchical
        + fitness
            * pop_size
            * best_fit
            * mean_elite_fit
            * mean_fit
            * worst_fit
            * stdev_fit
        + diversity
            * allele_sdi
            * chrom_sdi
        + performance
            + overall
            + elites


"""


def population_statistics(population):

    # get population size
    pop_size = len(population)

    # get population data; list of fitness
    pop_fit_data = [citizen.fitness() for citizen in population]

    # get population sum fitness
    sum_fit = sum(pop_fit_data)

    # get population best fitness
    best_fit = max(pop_fit_data)  # population[0].fitness()

    # get population worst fitness
    worst_fit = min(pop_fit_data)  # population[pop_size - 1].fitness()

    # get population mean fitness
    mean_fit = sum_fit / pop_size

    # get population standard deviation
    std = population_stand_dev(pop_fit_data, mean_fit)

    # get allele and chromosome diversities
    allele_diversity, chromosome_diversity = population_diversity(population)

    # get previous population elites' mean fitness
    elites_overall_stats, elites_stats = analyze_elite_performance(population)

    # get elite fitness stats
    elite_fit_data = list([])
    sum_elite_fit = 0
    best_elite_fit = 0
    worst_elite_fit = 0
    mean_elite_fit = 0
    elite_std = 0
    if elites_stats is not None:
        elite_fit_data.extend([elite_stat["fitness"] for elite_stat in elites_stats])

        sum_elite_fit = sum(elite_fit_data)
        best_elite_fit = max(elite_fit_data)
        worst_elite_fit = min(elite_fit_data)
        mean_elite_fit = sum_elite_fit / len(elite_fit_data)
        elite_std = population_stand_dev(elite_fit_data, mean_elite_fit)

    # create dictionary object
    stats_dict = dict([])
    stats_dict["sum_fit"] = sum_fit
    stats_dict["best_fit"] = best_fit
    stats_dict["worst_fit"] = worst_fit
    stats_dict["mean_fit"] = mean_fit
    stats_dict["std_fit"] = std

    stats_dict["sum_elite_fit"] = sum_elite_fit
    stats_dict["best_elite_fit"] = best_elite_fit
    stats_dict["worst_elite_fit"] = worst_elite_fit
    stats_dict["mean_elite_fit"] = mean_elite_fit
    stats_dict["std_elite_fit"] = elite_std

    stats_dict["allele_sdi"] = allele_diversity
    stats_dict["chrom_sdi"] = chromosome_diversity
    stats_dict["elites_overall_stats"] = elites_overall_stats
    stats_dict["elites_stats"] = elites_stats
    stats_dict["market_stats"] = None

    return stats_dict


def population_stand_dev(pop_fitnesses, mean_fitness):
    sum_sq_var = 0
    for fitness in pop_fitnesses:
        variance = fitness - mean_fitness
        sq_var = pow(variance, 2)
        sum_sq_var += sq_var

    variance = sum_sq_var / (len(pop_fitnesses) - 1)
    stand_dev = pow(variance, 0.5)

    return stand_dev


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


def analyze_elite_performance(population):

    # obtain previous generation's elites from population; only get their fitness
    elites_stats = list([])
    for citizen in population:
        if citizen.is_elite:
            elites_stats.append(citizen.account.metrics())

    # get elite count
    elite_count = len(elites_stats)
    if elite_count == 0:
        return None, None

    # sum all elite stats then calculate mean
    sum_elite_stats = elites_stats[0].copy()
    for i in range(1, elite_count - 1):
        sum_dict(sum_elite_stats, elites_stats[i])

    # average only the "avg_stat" keys
    average_dict(sum_elite_stats, len(elites_stats))

    # done; return elites mean fitness
    return sum_elite_stats, elites_stats


def sum_dict(dict1, dict2):
    for key, value in dict2.items():
        if isinstance(value, dict):
            sum_dict(dict1[key], value)
        else:
            if "most" in key or "high" in key:
                dict1[key] = max(dict1[key], dict2[key])
            else:
                dict1[key] += value


def average_dict(d, count):
    for key, value in d.items():
        if isinstance(value, dict):
            average_dict(d[key], count)
        else:
            if "avg" in key or "pct" in key or "fitness" in key:
                d[key] /= count



