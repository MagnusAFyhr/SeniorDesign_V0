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
from genetics.chromosome import chromosome as chrom
from genetics.allele.helper import allele_build as ale_bui
from genetics.chromosome.helper import chrom_build as chr_bui
import random


def generate_random_population(pop_size, debug_mode):
    # Create Empty List
    random_pop = list([])

    # Initialize & Append Random Individuals
    for i in range(0, pop_size):
        random_pop.append(indiv.Individual(debug=debug_mode))

    # Return Random Population
    return random_pop


def generate_normal_population(pop_size, debug_mode):

    # Create A Pool Of Available Technical Indicators
    avail_tech_ind = list([])
    for ti in params.AVAIL_TECH_IND.values():
        avail_tech_ind.append(ti)

    # Initialize A Normal Pool Of Alleles
    normal_allele_pool = list([])
    net_allele_count = pop_size * params.CHROM_ALLELE_COUNT
    for i in range(0, net_allele_count):
        tech_ind = avail_tech_ind[i % len(avail_tech_ind)]
        allele_encoding = ale_bui.random_encoding(tech_ind=tech_ind)
        normal_allele_pool.append(allele_encoding)

    # Initialize A Pool Of Chromosomes
    normal_chromosome_pool = list([])
    for i in range(0, pop_size):
        chrom_alleles = list([])
        # choose and pop random allele from pool; append to chrom_alleles
        for n in range(0, params.CHROM_ALLELE_COUNT):
            rand_allele_index = random.randint(0, len(normal_allele_pool) - 1)
            chrom_alleles.append(normal_allele_pool.pop(rand_allele_index))
        # initialize & append chromosome
        chromosome = chrom.Chromosome(chr_bui.random_encoding(chrom_alleles), debug=debug_mode)
        normal_chromosome_pool.append(chromosome)

    # Use Chromosomes To Initialize Individuals
    normal_individuals = list([])
    for i in range(0, pop_size):
        normal_individuals.append(indiv.Individual(chromosome=normal_chromosome_pool.pop(), debug=debug_mode))

    return normal_individuals
