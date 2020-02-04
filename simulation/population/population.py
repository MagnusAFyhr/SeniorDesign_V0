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

TO-DO :
    - verify() method for population?           :
    - diversity tracking                        :
        + should average diversity across all allele variables
    - add debug to this class                   :
    - make population initialization not random :


"""

import simulation.population.helper.pop_evaluate as pop_eval
import simulation.population.helper.pop_statistics as pop_stat

import genetics.chromosome.chromosome as chrom
import phenetics.individual.individual as indiv

import time


class Population:

    initialized = False
    _debug_mode = 0

    """
    Initialize Population
    """
    def __init__(self, pop_size, debug=0):

        self._debug_mode = debug

        # initialize random population
        self.citizens = self.initialize_random_population(pop_size)
        self.size = pop_size
        self.gen_count = 1
        self.step_count = 0
        self.iter_count = 0
        self.birth_date = None
        self.last_date = None

        # Done Initializing!
        self.initialized = True
        return

    """
    Simulates A Step In The Population With A Given Observation
    """
    def step(self, observation):

        for citizen in self.citizens:
            if self.step_count == 0:
                self.birth_date = observation['Date']
            citizen.step(observation)
            self.iter_count += 1
            self.last_date = observation['Date']

        self.step_count += 1

        return

    """
    Generates The Next Population
    """
    def next_generation(self):

        # get population statistics
        if self._debug_mode > 1 and self._debug_mode != 5:
            print("\t\t< POP > : Calculating Population Statistics...")
        start_t = time.time_ns()

        statistics = self.metrics()
        statistics["gen_count"] = self.gen_count
        statistics["step_count"] = self.step_count
        statistics["iter_count"] = self.iter_count
        statistics["start_date"] = self.birth_date
        statistics["end_date"] = self.last_date

        end_t = time.time_ns()
        if self._debug_mode == 5:
            elapsed = end_t - start_t
            elapsed /= pow(10, 9)
            print("\t\t< POP > : Calculated Population Statistics : {} s.".format(elapsed))

        # get elites and parents from current population
        if self._debug_mode > 1 and self._debug_mode != 5:
            print("\t\t< POP > : Evaluating Population; Selecting Elites & Parents...")
        start_t = time.time_ns()

        elites, parents = self.evaluate()

        end_t = time.time_ns()
        if self._debug_mode == 5:
            elapsed = end_t - start_t
            elapsed /= pow(10, 9)
            print("\t\t< POP > : Evaluated Population; Selected Elites & Parents : {} s.".format(elapsed))

        # create offspring from parents
        if self._debug_mode > 1 and self._debug_mode != 5:
            print("\t\t< POP > : Producing Offspring; Applying Crossovers...")
        start_t = time.time_ns()

        offspring = self.reproduce(parents)
        offspring = offspring[len(elites):]
        offspring.extend([elite.clone() for elite in elites])  # append elite clones to offspring

        end_t = time.time_ns()
        if self._debug_mode == 5:
            elapsed = end_t - start_t
            elapsed /= pow(10, 9)
            print("\t\t< POP > : Produced Offspring; Applied Crossovers : {} s.".format(elapsed))

        # apply mutations to offspring
        if self._debug_mode > 1 and self._debug_mode != 5:
            print("\t\t< POP > : Modifying Offspring; Applying Mutations...")
        start_t = time.time_ns()

        offspring = self.modify(offspring)

        end_t = time.time_ns()
        if self._debug_mode == 5:
            elapsed = end_t - start_t
            elapsed /= pow(10, 9)
            print("\t\t< POP > : Modified Offspring; Applied Mutations : {} s.".format(elapsed))

        # create new set of population citizens
        if self._debug_mode > 1 and self._debug_mode != 5:
            print("\t\t< POP > : Initializing Next Population...")
        start_t = time.time_ns()

        self.citizens.clear()
        self.citizens = [indiv.Individual(chromosome=chromosome, debug=self._debug_mode) for chromosome in offspring]

        end_t = time.time_ns()
        if self._debug_mode == 5:
            elapsed = end_t - start_t
            elapsed /= pow(10, 9)
            print("\t\t< POP > : Initialized Next Population : {} s.".format(elapsed))

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
            mod_chromosome = chrom.Chromosome(encoding, debug=self._debug_mode)
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
            random_pop.append(indiv.Individual(debug=self._debug_mode))

        # return random population
        return random_pop
