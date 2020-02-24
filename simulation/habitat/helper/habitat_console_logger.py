"""

Title : habitat_console_logger.py
Author : Magnus Fyhr
Created : 02/17/2020

Purpose :


Development :


Testing :


Cleaning :


Optimizing :


TO-DO:


"""

import analysis.parameters as params


def report(gen_stats, debug_mode):

    # Generic Header
    if debug_mode in params.HABITAT_CONSOLE:
        report_generic_header(gen_stats)

    # General Population Statistics Report
    if debug_mode in params.HABITAT_CONSOLE:
        report_fitness_statistics(gen_stats)
        report_diversity_statistics(gen_stats)

    # General Market Statistics Report
    if debug_mode in params.ACCOUNT_CONSOLE:
        if None is not None:
            # report_market_statistics( ??? )
            pass

    # Detailed Elite Statistics Report
    if debug_mode in params.ACCOUNT_CONSOLE:
        if gen_stats["elites_overall_stats"] is not None:
            report_elite_statistics(
                gen_stats["elites_overall_stats"]["general"],
                gen_stats["elites_overall_stats"]["technical"]
            )

    return


def report_generic_header(gen_stats):
    print("\t< HAB > : General Information.")
    print("\t\t<     > : Generation\t\t\t\t\t: {} ".format(gen_stats["gen_count"]))
    print("\t\t<     > : Population Size\t\t\t\t: {}".format(gen_stats["pop_size"]))
    print("\t\t<     > : Runtime\t\t\t\t\t\t: {} seconds".format(round(gen_stats["runtime"], 4)))
    print("\t\t<     > : Open Date\t\t\t\t\t\t: {} ".format(gen_stats["open_date"]))
    print("\t\t<     > : Close Date\t\t\t\t\t: {} ".format(gen_stats["close_date"]))
    print("\t\t<     > : Duration\t\t\t\t\t\t: {} days".format(gen_stats["step_count"]))

    return


def report_fitness_statistics(gen_stats):
    print("\t< HAB > : Fitness Statistics. ")
    print("\t\t<     > : Best Fitness\t\t\t\t\t: {}".format(round(gen_stats["best_fit"], 4)))
    print("\t\t<     > : Mean Fitness\t\t\t\t\t: {}".format(round(gen_stats["mean_fit"], 4)))
    print("\t\t<     > : Worst Fitness\t\t\t\t\t: {}".format(round(gen_stats["worst_fit"], 4)))
    print("\t\t<     > : Fitness Std. Dev.\t\t\t\t: {}".format(round(gen_stats["fit_stdev"], 4)))
    print("\t\t<     > : Mean Elite Fitness\t\t\t: {}".format(round(gen_stats["mean_elite_fit"], 4)))
    print("\t\t<     > : Market Fitness\t\t\t\t: {}".format(round(gen_stats["market_fit"], 4)))

    return


def report_diversity_statistics(gen_stats):
    print("\t< HAB > : Diversity Statistics. ")
    print("\t\t<     > : Allele Diversity\t\t\t\t: {}%".format(round(gen_stats["allele_sdi"] * 100, 2)))
    print("\t\t<     > : Chromosome Diversity\t\t\t: {}%".format(round(gen_stats["chrom_sdi"] * 100, 2)))


def report_market_statistics(market_stats):
    print("\t< HAB > : Market Statistics. ")

    return


def report_elite_statistics(general_elite_stats, technical_elite_stats):
    print("\t< HAB > : Elite Statistics. ")

    base_string = "\t\t<     > : "

    __print_next_nested_dict(base_string, general_elite_stats)

    return


def __print_next_nested_dict(base_string, nested_dict):
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            print("{}{}: ".format(base_string, key))
            __print_next_nested_dict("\t" + base_string, value)
        else:
            print("{}{:<20}: {}".format(base_string, key, round(value, 4)))
