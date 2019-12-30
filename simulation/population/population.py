"""

Title : population.py
Author : Magnus Fyhr
Created : 12/17/2019

Purpose : The Population class object, responsible for simulating a defined
            set of Individuals generationally, implementing proper Darwinian
            evolution.

Development :
    - init                          : DONE
    - step                          : DONE
    - next_generation               : DONE
    - reproduce                     : DONE
    - modify                        : DONE
    - evaluate                      : DONE
    - statistics                    : DONE
    - initialize_rand_population    : DONE

Testing :
    - init                          : DONE
    - step                          : DONE
    - next_generation               : DONE
    - reproduce                     : DONE
    - modify                        : DONE
    - evaluate                      : DONE
    - statistics                    : DONE
    - initialize_rand_population    : DONE


"""

import simulation.population.helper.pop_evaluate as pop_eval
import simulation.population.helper.pop_statistics as pop_stat

import genetics.chromosome.chromosome as chrom
import phenetics.individual.individual as indiv


class Population:

    """
    Initialize Population
    """
    def __init__(self, pop_size):
        # initialize random population
        self.citizens = self.initialize_random_population(pop_size)
        self.size = pop_size
        self.gen_count = 0
        self.step_count = 0
        self.iter_count = 0

    """
    Simulates A Step In The Population With A Given Observation
    """
    def step(self, observation):

        for citizen in self.citizens:
            citizen.step(observation)
            self.iter_count += 1

        self.step_count += 1

        return

    """
    Generates The Next Population
    """
    def next_generation(self):

        # get population statistics
        statistics = self.metrics()
        statistics["gen_count"] = self.gen_count
        statistics["step_count"] = self.step_count
        statistics["iter_count"] = self.iter_count

        # get elites and parents from current population
        elites, parents = self.evaluate()

        # create offspring from parents
        offspring = self.reproduce(parents)

        # append elite clones to offspring
        offspring.extend([elite.clone() for elite in elites])

        # apply mutations to offspring
        offspring = self.modify(offspring)

        # create new set of population citizens
        self.citizens.clear()
        self.citizens = [indiv.Individual(chromosome) for chromosome in offspring]

        self.iter_count = 0
        self.step_count = 0
        self.gen_count += 1

        # return statistics; for system feedback
        return statistics

    """
    Selection Mechanism For The Population 
    """
    def evaluate(self):
        # Determine Elites & Parents For Offspring; Return [Elites, Parents]
        return pop_eval.evaluate_individuals(self.citizens)

    """
    Reproduction Mechanism For The Population 
    """
    def reproduce(self, parents):
        pool = parents.copy()
        offspring = list([])

        # iterate; until there are no longer at least 2 parents
        while len(pool) > 1:
            # select alpha parent
            parent_a = pool.pop()

            # select beta parent
            parent_b = pool.pop()

            # create offspring pair
            pair = parent_a.mate(parent_b)

            # append offspring
            offspring.extend(pair)

            # iterate
            continue

        return offspring

    """
    Mutation Operator For The Population
    """
    def modify(self, offspring):
        mod_offspring = list([])

        for chromosome in offspring:
            encoding = chromosome.mutate()
            mod_chromosome = chrom.Chromosome(encoding)
            mod_offspring.append(mod_chromosome)

        return mod_offspring

    """
    Calculate The Population Metrics
    """
    def metrics(self):
        # Return Statistics JSON Object
        return pop_stat.population_statistics(self.citizens)

    """
    Initialize A Random Population Of Individuals 
        - might want to implement logic to force evenly distributed population
    """
    def initialize_random_population(self, pop_size):
        random_pop = list([])

        # initialize & append individuals
        for i in range(0, pop_size):
            random_pop.append(indiv.Individual())

        # return random population
        return random_pop
