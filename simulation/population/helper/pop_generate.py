"""

Title : pop_generate.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose :


Development :


Testing :


"""
import analysis.parameters as params
from phenetics.individual import individual as indiv
from genetics.allele.helper import allele_build as ale_bui


def generate_random_population(pop_size, debug_mode):
    # Create Empty List
    random_pop = list([])

    # Initialize & Append Random Individuals
    for i in range(0, pop_size):
        random_pop.append(indiv.Individual(debug=debug_mode))

    # Return Random Population
    return random_pop


def generate_normal_population(pop_size):
    # Create Empty List
    normal_pop = list([])

    # Create A Pool Of Available Technical Indicators
    avail_tech_ind = list([])
    for ti in params.AVAIL_TECH_IND.values():
        avail_tech_ind.append(ti)

    # Initialize A Normal Pool Of Alleles
    normal_allele_pool = list([])
    net_allele_count = pop_size * params.CHROM_ALLELE_COUNT
    for i in net_allele_count:
        tech_ind = avail_tech_ind[i % len(avail_tech_ind)]
        allele_encoding = ale_bui.random_encoding(tech_ind=tech_ind)
        normal_allele_pool.append(allele_encoding)

    # Initialize A Pool Of Chromosomes

    # Use Chromosomes To Initialize Individuals

    pass
